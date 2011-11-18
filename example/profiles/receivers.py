from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django_stripe.shortcuts import stripe
from django_stripe.contrib.registration.backends import StripeSubscriptionBackend
from django_stripe.contrib.registration.signals import user_registered
from django_stripe.signals import (upcoming_invoice_updated, invoice_ready, \
    recurring_payment_failed, subscription_final_payment_attempt_failed, StripeWebhook)

from .models import UserProfile

@receiver(post_save, sender=User, \
    dispatch_uid='profiles.receivers.create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)

@receiver(user_registered, sender=StripeSubscriptionBackend, \
    dispatch_uid='profiles.receivers.link_stripe_customer')
def link_stripe_customer(sender, user, request, customer, plan=None, **kwargs):
    user_profile = user.get_profile()
    user_profile.customer_id = customer.id
    user_profile.card_last4 = customer.active_card.last_4
    user_profile.plan = plan

    try:
        user_profile.trial_end = datetime.utcfromtimestamp(customer.subscription.trial_end)
    except AttributeError:
        pass

    user_profile.save()

    upcoming_invoice_updated.send(sender=None, customer=customer)

@receiver(invoice_ready, sender=StripeWebhook, \
    dispatch_uid='profiles.receivers.invoice_user')
def invoice_user(sender, customer, invoice, **kwargs):
    try:
        user_profile = UserProfile.objects.get(customer_id=customer)
        amount = int(user_profile.collaborator_count * user_profile.get_price())

        if not user_profile.trialing and amount > 0:
            stripe.InvoiceItem.create( \
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description="%s Collaborators" \
                                % user_profile.collaborator_count
            )

            upcoming_invoice_updated.send(sender=None, customer=customer)

    except UserProfile.DoesNotExist:
        pass

@receiver(recurring_payment_failed, sender=StripeWebhook, \
    dispatch_uid='profiles.receviers.update_payment_attempts')
def update_payment_attempts(sender, customer, attempt, payment, **kwargs):
    try:
        user_profile = UserProfile.objects.get(customer_id=customer)
        user_profile.payment_attempts = int(attempt)
        user_profile.last_payment_attempt = datetime.utcfromtimestamp(payment['time'])
        user_profile.save()
    except UserProfile.DoesNotExist:
        pass

@receiver(subscription_final_payment_attempt_failed, sender=StripeWebhook, \
    dispatch_uid='profiles.receviers.lock_account')
def lock_account(sender, customer, subscription, **kwargs):
    try:
        user = User.objects.get(profile__customer_id=customer)
        user.is_active = False
        user.save()
    except User.DoesNotExist:
        pass

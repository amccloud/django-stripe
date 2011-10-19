from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django_stripe.contrib.registration.signals import user_registered
from django_stripe.contrib.registration.backends import StripeSubscriptionBackend
from django_stripe.signals import (recurring_payment_failed, \
    subscription_final_payment_attempt_failed, StripeWebhook)

from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)

@receiver(user_registered, sender=StripeSubscriptionBackend)
def link_stripe_customer(sender, user, request, customer, last4, plan=None, **kwargs):
    user_profile = user.get_profile()
    user_profile.customer_id = customer.id
    user_profile.card_last4 = last4
    user_profile.plan = plan

    try:
        user_profile.trial_end = datetime.fromtimestamp(customer.subscription.trial_end)
    except AttributeError:
        pass

    user_profile.save()

@receiver(recurring_payment_failed, sender=StripeWebhook)
def update_payment_attempts(sender, customer, attempt, payment, **kwargs):
    try:
        user_profile = UserProfile.objects.get(customer_id=customer)
        user_profile.payment_attempts = int(attempt)
        user_profile.last_payment_attempt = datetime.fromtimestamp(payment['time'])
        user_profile.save()
    except UserProfile.DoesNotExist:
        pass

@receiver(subscription_final_payment_attempt_failed, sender=StripeWebhook)
def lock_account(sender, customer, subscription, **kwargs):
    try:
        user = User.objects.get(profile__customer_id=customer)
        user.is_active = False
        user.save()
    except User.DoesNotExist:
        pass

from django.utils.functional import curry
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django_stripe.shortcuts import stripe
from django_stripe.settings import STRIPE_CUSTOMER_DESCRIPTION

from registration.backends.simple import SimpleBackend

from .forms import StripeSubscriptionForm
from .signals import user_registered

class StripeSubscriptionBackend(SimpleBackend):
    def get_form_class(self, request):
        return curry(StripeSubscriptionForm, initial={
            'plan': request.GET.get('plan'),
        })

    def get_customer_description(self, user):
        return STRIPE_CUSTOMER_DESCRIPTION(user)

    def register(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password1']
        email = kwargs['email']
        token = kwargs['token']
        plan = kwargs['plan']

        User.objects.create_user(username, email, password)
        new_user = authenticate(username=username, password=password)
        login(request, new_user)

        customer = stripe.Customer.create(
            description=self.get_customer_description(new_user),
            card=token,
            plan=plan
        )

        user_registered.send(**{
            'sender': self.__class__,
            'user': new_user,
            'request': request,
            'customer': customer,
            'plan': plan,
        })

        return new_user

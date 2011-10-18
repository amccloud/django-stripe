import stripe

from django.utils.functional import curry
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django_stripe.settings import STRIPE_SECRET_KEY

from registration.backends.simple import SimpleBackend

from .forms import StripeSubscriptionForm
from .signals import user_registered
from .settings import SUBSCRIPTION_CUSTOMER_DESCRIPTION

stripe.api_key = STRIPE_SECRET_KEY

class StripeSubscriptionBackend(SimpleBackend):
    def get_form_class(self, request):
        return curry(StripeSubscriptionForm, initial={
            'plan': request.GET.get('plan'),
        })

    def get_customer_description(self, user):
        return SUBSCRIPTION_CUSTOMER_DESCRIPTION(user)

    def register(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password1']
        email = kwargs['email']
        token = kwargs['token']
        last4 = kwargs['last4']
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
            'last4': last4,
            'plan': plan,
        })

        return new_user

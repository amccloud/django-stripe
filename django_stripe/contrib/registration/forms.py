from django import forms

from registration.forms import RegistrationForm

from django_stripe.forms import TokenForm

from .settings import SUBSCRIPTION_PLAN_CHOICES

class StripeSubscriptionForm(RegistrationForm, TokenForm):
    plan = forms.CharField(widget=forms.Select(choices=SUBSCRIPTION_PLAN_CHOICES))

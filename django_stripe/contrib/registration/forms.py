from django_stripe.settings import *
from django_stripe.forms import PlanSubscriptionForm
from registration.forms import RegistrationForm

class CreditCardRegistrationForm(RegistrationForm, PlanSubscriptionForm):
    pass

from django_stripe.settings import *
from django_stripe.forms import CreditCardForm
from registration.forms import RegistrationForm

class CreditCardRegistrationForm(RegistrationForm, CreditCardForm):
    pass

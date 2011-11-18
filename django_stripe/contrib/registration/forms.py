from registration.forms import RegistrationForm

from django_stripe.forms import CustomerForm

class StripeSubscriptionForm(RegistrationForm, CustomerForm):
    pass

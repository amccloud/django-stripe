import datetime, stripe
from django import forms
from django.utils.translation import ugettext as _
from django_stripe.settings import *

CURRENT_YEAR = datetime.date.today().year
MONTH_CHOICES = [(i, '%02d' % i) for i in range(01, 13)]
YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

class CreditCardForm(forms.Form):
    number = forms.CharField(label=_('Card number'))
    exp_month = forms.CharField(widget=forms.Select(choices=MONTH_CHOICES), label=_('Expiration month'))
    exp_year = forms.CharField(widget=forms.Select(choices=YEAR_CHOICES), label=_('Expiration year'))
    cvc = forms.CharField(label=_('Security code'))

    def get_stripe_data(self):
        return {
            'validate': STRIPE_VALIDATE_CARD,
            'description': self.cleaned_data['username'],
            'card': {
                'number': self.cleaned_data['number'],
                'exp_month': self.cleaned_data['exp_month'],
                'exp_year': self.cleaned_data['exp_year'],
                'cvc': self.cleaned_data['cvc'],
            },
        }

    def create_stripe_customer(self):
        stripe.api_key = STRIPE_PRIVATE_KEY
        try:
            stripe.Customer.create(**self.get_stripe_data())
        except stripe.StripeError, e:
            self._errors[e.param] = self.error_class([str(e)])
            if e.param in self.cleaned_data:
                del self.cleaned_data[e.param]

    def _post_clean(self):
        super(CreditCardForm, self)._post_clean()
        if self._errors:
            return
        self.create_stripe_customer()

class PlanSubscriptionForm(CreditCardForm):
    plan = forms.CharField(widget=forms.Select(choices=STRIPE_PLAN_CHOICES))
    code = forms.CharField(required=False, label=_('Coupon'))

    def get_stripe_data(self):
        data = super(PlanSubscriptionForm, self).get_stripe_data()
        data['plan'] = self.cleaned_data['plan']
        code = self.cleaned_data['code']
        if code:
            data['coupon'] = code
        return data

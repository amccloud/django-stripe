import types, datetime

from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField
from django.utils.translation import ugettext as _

from .settings import STRIPE_PLAN_CHOICES, STRIPE_CUSTOMER_DESCRIPTION
from .shortcuts import stripe

FORM_PREIX = 'stripe'

CURRENT_YEAR = datetime.date.today().year
MONTH_CHOICES = [(i, '%02d' % i) for i in xrange(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

def make_widget_anonymous(widget):
    def _anonymous_render(instance, name, value, attrs=None):
        return instance._orig_render('', value, attrs)

    widget._orig_render = widget.render
    widget.render = types.MethodType(_anonymous_render, widget)

    return widget

class CardForm(forms.Form):
    number = forms.CharField(label=_("Card number"))
    exp_month = forms.CharField(label=_("Expiration month"), widget=forms.Select(choices=MONTH_CHOICES))
    exp_year = forms.CharField(label=_("Expiration year"), widget=forms.Select(choices=YEAR_CHOICES))

    def get_cvc_field(self):
        return forms.CharField(label=_("Security code (CVV)"))

    def get_address_line1_field(self):
        return forms.CharField(label=_("Address"))

    def get_address_zip_field(self):
        return USZipCodeField(label=_("Zipcode"))

    def __init__(self, validate_cvc=True, validate_address=False, \
                    prefix=FORM_PREIX, *args, **kwargs):
        super(CardForm, self).__init__(prefix=prefix, *args, **kwargs)

        if validate_cvc:
            self.fields['cvc'] = self.get_cvc_field()

        if validate_address:
            self.fields['address_line1'] = self.get_address_line1_field()
            self.fields['address_zip'] = self.get_address_zip_field()


class AnonymousCardForm(CardForm):
    def __init__(self, *args, **kwargs):
        super(AnonymousCardForm, self).__init__(*args, **kwargs)

        for key in self.fields.keys():
            make_widget_anonymous(self.fields[key].widget)


class CardTokenForm(AnonymousCardForm):
    last4 = forms.CharField(min_length=4, max_length=4, required=False, widget=forms.HiddenInput())
    token = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, prefix=FORM_PREIX, *args, **kwargs):
        super(CardTokenForm, self).__init__(prefix=prefix, *args, **kwargs)

    def clean(self):
        if not self.cleaned_data['last4'] or not self.cleaned_data['token']:
            raise forms.ValidationError(_("Could not validate credit card."))


class CustomerForm(CardTokenForm):
    plan = forms.CharField(widget=forms.Select(choices=STRIPE_PLAN_CHOICES))

    def get_customer_description(self, user):
        return STRIPE_CUSTOMER_DESCRIPTION(user)

    def save(self, user):
        return stripe.Customer.create(
            description=self.get_customer_description(user),
            card=self.cleaned_data['token'],
            plan=self.cleaned_data['plan']
        )

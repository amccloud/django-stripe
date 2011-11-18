from stripe import convert_to_stripe_object

from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, FormView

from .settings import STRIPE_SECRET_KEY
from .forms import CardTokenForm
from .signals import (recurring_payment_failed, invoice_ready, \
    recurring_payment_succeeded, subscription_trial_ending, \
    subscription_final_payment_attempt_failed, ping, StripeWebhook)

class BaseCardTokenFormView(FormView):
    template_name = 'django_stripe/card_form.html'
    form_class = CardTokenForm

    def get_last4(self):
        return None

    def get_form_kwargs(self):
        kwargs = super(BaseCardTokenFormView, self).get_form_kwargs()
        kwargs.update({
            'initial': {
                'last4': self.get_last4(),
            }
        })

        return kwargs

class WebhookSignalView(View):
    http_method_names = ['post']
    event_signals = {
        'recurring_payment_failed': recurring_payment_failed,
        'invoice_ready': invoice_ready,
        'recurring_payment_succeeded': recurring_payment_succeeded,
        'subscription_trial_ending': subscription_trial_ending,
        'subscription_final_payment_attempt_failed': subscription_final_payment_attempt_failed,
        'ping': ping,
    }

    def post(self, request, *args, **kwargs):
        if 'json' not in request.POST:
            raise Http404

        message = json.loads(request.POST.get('json'))
        event = message.get('event')
        del message['event']

        if event not in self.event_signals:
            raise Http404

        for key, value in message.iteritems():
            if isinstance(value, dict) and 'object' in value:
                message[key] = convert_to_stripe_object(value, STRIPE_SECRET_KEY)

        signal = self.event_signals.get(event)
        signal.send_robust(sender=StripeWebhook, **message)

        return HttpResponse()

webhook_to_signal = csrf_exempt(WebhookSignalView.as_view())

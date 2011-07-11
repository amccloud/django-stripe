from django.http import Http404
from django.utils import simplejson as json
from .signals import *

EVENT_SIGNAL_MAP = {
    'subscription_trial_ending': subscription_trial_ending,
    'recurring_payment_succeeded': recurring_payment_succeeded,
    'recurring_payment_failed': recurring_payment_failed,
    'subscription_final_payment_attempt_failed': subscription_final_payment_attempt_failed,
}

def webhook_to_signal(request):
    if 'json' not in request.POST:
        raise Http404
    message = json.loads(request.POST.get('json'))
    print message
    event = message.get('event')
    if event not in EVENT_SIGNAL_MAP:
        raise Http404
    signal = EVENT_SIGNAL_MAP.get(event)
    signal.send(sender=webhook_to_signal, message=message)

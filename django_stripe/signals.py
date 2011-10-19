from django.dispatch import Signal

class StripeWebhook(object):
    pass

recurring_payment_failed = Signal(providing_args=[
    'customer', 'attempt', 'invoice', 'payment', 'livemode', 
])

invoice_ready = Signal(providing_args=[
    'customer', 'invoice',
])

recurring_payment_succeeded = Signal(providing_args=[
    'customer', 'invoice', 'payment', 'livemode',
])

subscription_trial_ending = Signal(providing_args=[
    'customer', 'subscription',
])

subscription_final_payment_attempt_failed = Signal(providing_args=[
    'customer', 'subscription',
])

ping = Signal()

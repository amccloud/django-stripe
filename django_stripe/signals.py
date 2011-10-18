import django.dispatch

__all__ = ['recurring_payment_failed', 'invoice_ready', \
            'recurring_payment_succeeded', 'subscription_trial_ending', \
            'subscription_final_payment_attempt_failed', 'ping']

recurring_payment_failed = django.dispatch.Signal(providing_args=[
    'customer', 'livemode', 'event', 'attempt', 'invoice', 'payment',
])

invoice_ready = django.dispatch.Signal(providing_args=[
    'customer', 'event', 'invoice',
])

recurring_payment_succeeded = django.dispatch.Signal(providing_args=[
    'customer', 'livemode', 'event', 'invoice', 'payment',
])

subscription_trial_ending = django.dispatch.Signal(providing_args=[
    'customer', 'event', 'subscription',
])

subscription_final_payment_attempt_failed = django.dispatch.Signal(providing_args=[
    'customer', 'event', 'subscription',
])

ping = django.dispatch.Signal(providing_args=[
    'event',
])

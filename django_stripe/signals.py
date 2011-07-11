import django.dispatch

subscription_trial_ending = django.dispatch.Signal(providing_args=['message'])
recurring_payment_succeeded = django.dispatch.Signal(providing_args=['message'])
recurring_payment_failed = django.dispatch.Signal(providing_args=['message'])
subscription_final_payment_attempt_failed = django.dispatch.Signal(providing_args=['message'])

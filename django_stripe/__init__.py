from django.dispatch import receiver
from .signals import *

@receiver(subscription_trial_ending)
def _subscription_trial_ending(sender, message, **kwargs):
    print message

@receiver(recurring_payment_succeeded)
def _recurring_payment_succeeded(sender, message, **kwargs):
    print message

@receiver(recurring_payment_failed)
def _recurring_payment_failed(sender, message, **kwargs):
    print message

@receiver(subscription_final_payment_attempt_failed)
def _subscription_final_payment_attempt_failed(sender, message, **kwargs):
    print message

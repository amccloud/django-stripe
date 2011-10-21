from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from django_stripe.contrib.registration.settings import SUBSCRIPTION_PLAN_CHOICES

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', unique=True)
    plan = models.CharField(max_length=32, choices=SUBSCRIPTION_PLAN_CHOICES, blank=True, null=True)
    customer_id = models.CharField(max_length=32, blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    payment_attempts = models.PositiveIntegerField(default=0, blank=True, null=True)
    last_payment_attempt = models.DateTimeField(blank=True, null=True)
    trial_end = models.DateTimeField(blank=True, null=True)

    @property
    def trialing(self):
        return datetime.now() >= self.trial_end

    @property
    def collaborator_count(self):
        return 4

    def get_price(self):
        if self.plan == 'pro':
            return 8.00

        return 0.00

    def __unicode__(self):
        return unicode(self.user)

from .receivers import *

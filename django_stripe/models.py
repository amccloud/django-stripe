from django.db import models

from .managers import InvoiceManager

class Invoice(models.Model):
    customer_id = models.CharField(max_length=32)
    stripe_id = models.CharField(max_length=32, blank=True, null=True)
    lines = models.TextField(blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    attempted = models.NullBooleanField(blank=True, default=False)
    closed = models.NullBooleanField(blank=True, default=False)
    paid = models.NullBooleanField(blank=True, default=False)
    created = models.DateTimeField(blank=True, null=True)

    objects = InvoiceManager()

    @property
    def subtotal_usd(self):
        return u"$%.2f" % (self.subtotal / 100,)

    @property
    def total_usd(self):
        return u"$%.2f" % (self.total / 100,)

from .receivers import *

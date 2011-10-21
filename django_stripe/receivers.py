from django.dispatch import receiver

from .shortcuts import stripe
from .models import Invoice
from .signals import (upcoming_invoice_updated, invoice_updated, \
                        invoice_ready, StripeWebhook)

@receiver(upcoming_invoice_updated, \
    dispatch_uid='django_stripe.receivers.sync_upcoming_invoice')
def sync_upcoming_invoice(sender, customer, **kwargs):
    invoice = stripe.Invoice.upcoming(customer=customer.id)
    invoice_updated.send(sender=None, invoice=invoice, refresh=False)

@receiver(invoice_updated, \
    dispatch_uid='django_stripe.receivers.sync_invoice')
def sync_invoice(sender, invoice, refresh=True, **kwargs):
    if refresh:
        invoice.refresh()

    Invoice.objects.sync(invoice)

@receiver(invoice_ready, sender=StripeWebhook, \
    dispatch_uid='django_stripe.receivers._invoice_ready')
def _invoice_ready(sender, customer, **kwargs):
    upcoming_invoice_updated.send_robust(sender=sender, customer=customer)

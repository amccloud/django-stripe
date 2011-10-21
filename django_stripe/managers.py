from django.db import models

class InvoiceManager(models.Manager):
    def sync(self, stripe_invoice):
        customer_id = stripe_invoice.customer
        stripe_id = stripe_invoice.get('id', None)

        defaults = {
            'customer_id': customer_id,
            'stripe_id': stripe_id,
            # 'lines': stripe_invoice.get('lines'),
            'subtotal': stripe_invoice.get('subtotal'),
            'total': stripe_invoice.get('total'),
            'attempted': stripe_invoice.get('attempted'),
            'closed': stripe_invoice.get('closed'),
            'paid': stripe_invoice.get('paid'),
            'created': stripe_invoice.get('created'),
        }

        filter_kwargs = {
            'stripe_id': None,
            'customer_id': customer_id,
            'defaults': defaults,
        }

        if stripe_id:
            filter_kwargs['stripe_id'] = stripe_id

        invoice, created = self.get_query_set().get_or_create(**filter_kwargs)

        if not created:
            invoice(**defaults)
            invoice.save()

        return invoice

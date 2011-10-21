from django.core.management.base import BaseCommand

from ...shortcuts import stripe

class Command(BaseCommand):
    help = "Clear all test customers from your stripe account."

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))
        count, offset = 100, 0

        if verbosity > 0:
            print "Clearing all test customers from your stripe account."

        while True:
            deleted = 0

            if verbosity > 1:
                print "Fetching customers %s-%s." % (offset, offset + count)

            customers = stripe.Customer.all(count=count, offset=offset).data

            if not customers:
                break

            for customer in customers:
                if customer.livemode:
                    continue

                if verbosity > 1:
                    print "Deleting customer %s, '%s'." % \
                        (customer.id, customer.description)

                customer.delete()
                deleted += 1

            offset += count - deleted

        if verbosity > 0:
            print "Done."

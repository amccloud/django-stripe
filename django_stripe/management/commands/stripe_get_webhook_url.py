from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = "A shortcut for copying your stripe wbehook url."

    def handle(self, *args, **options):
        current_site = Site.objects.get_current()

        try:
            print "http://%s%s" % (current_site, reverse('stripe:webhook'))
        except NoReverseMatch:
            print "Could not find url pattern for 'stripe:webhook'. " \
                    "Please include django_stripe.urls in your urlconf " \
                    "under the 'stripe' namespace."

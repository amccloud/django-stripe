from django.conf.urls.defaults import patterns, url

from django_stripe.settings import STRIPE_WEBHOOK_ENDPOINT

urlpatterns = patterns('django_stripe.views',
    url(STRIPE_WEBHOOK_ENDPOINT, 'webhook_to_signal', name='webhook'),
)

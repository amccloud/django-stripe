from django.conf.urls.defaults import *

urlpatterns = patterns('registration.views',
    url(r'register/$', 'register', {
        'backend': 'django_stripe.contrib.registration.backends.StripeSubscriptionBackend',
    }, name='registration_register'),
)

urlpatterns += patterns('',
    url(r'', include('registration.auth_urls')),
)

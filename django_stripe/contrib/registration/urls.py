from django.conf.urls.defaults import *

from django_stripe.forms import CreateTokenForm

urlpatterns = patterns('registration.views',
    url(r'register/$', 'register', {
        'backend': 'django_stripe.contrib.registration.backends.StripeSubscriptionBackend',
        'extra_context': {
            'create_token_form': CreateTokenForm(),
        },
    }, name='registration_register'),
)

urlpatterns += patterns('',
    url(r'', include('registration.auth_urls')),
)

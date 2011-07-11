from django.conf.urls.defaults import *
from .forms import CreditCardRegistrationForm

urlpatterns = patterns('registration.views',
    url(r'register/$', 'register', {
        'backend': 'django_stripe.contrib.registration.backends.StripeSubscriptionBackend',
        'form_class': CreditCardRegistrationForm,
    }, name='registration_register'),
)

urlpatterns += patterns('',
    url(r'', include('registration.auth_urls')),
)

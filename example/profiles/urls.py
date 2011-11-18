from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('profiles.views',
    url(r'^account/billing/$', 'account_billing_form', name='account_billing'),
)

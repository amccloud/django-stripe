from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^account/', include('django_stripe.contrib.registration.urls')),
    url(r'^account/', include('django_stripe.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

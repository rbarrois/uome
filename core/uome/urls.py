from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uome.views.home', name='home'),
    # url(r'^uome/', include('uome.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
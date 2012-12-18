from django.conf.urls import patterns, include, url

from newadmin import admin as newadmin
from django.contrib import admin


admin.autodiscover()
newadmin.autodiscover(True)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newadmin/', include(newadmin.urls())),
)

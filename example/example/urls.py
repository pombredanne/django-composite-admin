from django.conf.urls import patterns, include, url
from django.contrib import admin

from adminnext import admin as adminnext


admin.autodiscover()
adminnext.autodiscover(True)


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adminnext/', include(adminnext.urls())),
)

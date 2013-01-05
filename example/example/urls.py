from django.conf.urls import patterns, include, url
from django.contrib import admin

import adminnext


admin.autodiscover()
adminnext.site.autodiscover()

urls = adminnext.site._include_urls()
# print urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adminnext/', urls),
)

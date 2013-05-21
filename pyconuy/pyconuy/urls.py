from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = []
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',

    url(r'', include('main.urls', namespace='main')),
    url(r'', include('account.urls', namespace='account')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)


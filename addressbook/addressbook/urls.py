"""Primary URL's routing file."""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static as static_views
from contacts import views as contact_views


urlpatterns = [
    url(r'^$', contact_views.index, name='index'),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(.*)$', static_views.serve,
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^media/(.*)$', static_views.serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]

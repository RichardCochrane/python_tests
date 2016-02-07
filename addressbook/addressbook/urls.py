"""Primary URL's routing file."""

from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'contacts.views.index', name='index'),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^admin/', admin.site.urls),
)

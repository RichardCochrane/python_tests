"""URL's routing file for all contact urls except 'index' URL."""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^create/$', 'contacts.views.create', name='create_contact'),
    url(r'^update/(?P<contact_id>\d{1,10})/$', 'contacts.views.update', name='update_contact'),
    url(r'^delete/(?P<contact_id>\d{1,10})/$', 'contacts.views.delete', name='delete_contact'),
)

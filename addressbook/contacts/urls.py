"""URL's routing file for all contact urls except 'index' URL."""

from django.conf.urls import url

from contacts import views

app_name = 'contacts'

urlpatterns = [
    url(r'^create/details/$', views.create_details, name='create_contact_details'),
    url(r'^update/details/(?P<contact_id>\d{1,10})/$', views.update_details,
        name='update_contact_details'),
    url(r'^update/avatar/(?P<contact_id>\d{1,10})/$', views.update_avatar,
        name='update_contact_avatar'),
    url(r'^update/powers/(?P<contact_id>\d{1,10})/$', views.update_powers,
        name='update_contact_powers'),
    url(r'^delete/(?P<contact_id>\d{1,10})/$', views.delete, name='delete_contact'),
]

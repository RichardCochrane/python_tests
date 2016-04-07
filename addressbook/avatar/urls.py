from django.conf.urls import url

from avatar import views

app_name = 'avatar'

urlpatterns = [
    url(r'^add/$', views.add, name='avatar_add'),
    url(r'^render_primary/(?P<contact>[\w\d\@\.\-_]{3,30})/(?P<size>[\d]+)/$',
        views.render_primary, name='avatar_render_primary'),
    url(r'^list/(?P<codename>[\+\w\@\.]+)/(?P<id>[\d]+)/$', views.avatar, name='avatar'),
]

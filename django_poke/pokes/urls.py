from django.conf.urls import patterns, url

from pokes import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^user/new/$', views.NewUserView.as_view(), name='new_user'),
    url(r'^user/add/$', views.add_user, name='add_user'),
    url(r'^(?P<user_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<user_id>\d+)/poke/$', views.create_poke, name='create_poke'),
)
from django.conf.urls import patterns, url

from pokes import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.new_user, name='new_user'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<user_id>\d+)/$', views.create_poke, name='create_poke'),
)
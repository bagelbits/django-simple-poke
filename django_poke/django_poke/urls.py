from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^pokes/', include('pokes.urls', namespace="pokes")),
    url(r'^admin/', include(admin.site.urls)),
)
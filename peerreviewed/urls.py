from django.conf.urls import patterns, include, url
from django.contrib import admin
import browse.views as bviews

urlpatterns =\
    patterns('',
             url(r'^admin/', include(admin.site.urls)),

             # Prolly should move, but it's more of a browse thing
             url(r'^$', bviews.index, name="index"),

             # Other modules
             url(r'^browse/', include('browse.urls')),
             url(r'^new/', include('new.urls')),
             )

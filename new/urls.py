from django.conf.urls import patterns, url
import new.views as nviews


urlpatterns =\
    patterns('',
             url(r'^new/(professor|school|courne)$', nviews.new, name="new"),
             )

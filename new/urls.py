from django.conf.urls import patterns, include, url
from django.contrib import admin
import new.views as nviews


urlpatterns = patterns('',
    url(r'^new/(professor|school|courne)$', nviews.new, name="new"),
)

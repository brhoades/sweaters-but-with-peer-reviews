from django.conf.urls import patterns, include, url
from django.contrib import admin
import new.views as nviews


urlpatterns = patterns('',
    url(r'^(?P<page>(professor|review|course))$', nviews.new, name="new"),
)

from django.conf.urls import patterns, url
import new.views as nviews

urlpatterns = \
    patterns('',
             url(r'^(?P<page>(professor|review|course))$', nviews.new,
                 name="new"),
             )

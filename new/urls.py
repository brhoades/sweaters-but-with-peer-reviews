from django.conf.urls import patterns, url
import new.views as nviews

urlpatterns = \
    patterns('',
             url(r'^(?P<page>(school|department|professor|review|course))$',
                 nviews.new, name="new"),
             url(r'^add_vote$', nviews.addVote, name="addVote"),
             )

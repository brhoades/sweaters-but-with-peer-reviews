from django.conf.urls import patterns, include, url
from django.contrib import admin
import browse.views as bviews

urlpatterns = patterns('',
    url(r'^user/([0-9]+)?$', bviews.profile, name="profile"),
    url(r'^school/([0-9]+)?$', bviews.school, name="school"),
    url(r'^professor/([0-9]+)?$', bviews.professor, name="professor"),
    #               school      prof
    url(r'^review/([0-9]+)/([0-9]+)$', bviews.review, name="review_professor"),
    url(r'^review$', bviews.review_overview, name="reviews"),
)

from django.conf.urls import url
import new.views as nviews

urlpatterns = [
    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory|reviewcomment))$',
        nviews.new, name="new"),
    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory))/(?P<id>[0-9]+)$',
        nviews.edit, name="edit"),
    url(r'^add_vote$', nviews.addVote, name="addVote"),
]

from django.conf.urls import url
import new.views as nviews

urlpatterns = [
    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory|comment))$',
        nviews.new, name="new"),
    url(r'^add_vote$', nviews.addVote, name="addVote"),
]

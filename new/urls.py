from django.conf.urls import url
import new.views as nviews

urlpatterns = [
    url(r'^add_vote$', nviews.addVote, name="addVote"),
    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory|reviewcomment))$',
        nviews.new, name="new"),
    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory))/(?P<id>[0-9]+)$',
        nviews.edit, name="edit"),
    url(r'^report/(?P<model_name>[A-Za-z]+)/(?P<id>[0-9]+)$', nviews.report,
        name="new_report")
]

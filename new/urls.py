from django.conf.urls import url
import new.views as nviews
import browse.views as bviews
import accounts.views as accviews

urlpatterns = [
    url(r'^add_vote$', nviews.addVote, name="addVote"),
    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory|reviewcomment))$',
        nviews.new, name="new"),

    url(r'^peerreview/?$', bviews.peer_review, name="peerreview"),

    url(r'^(?P<page>(school|department|professor|review|course|field'
        '|fieldcategory|reviewcomment))/(?P<id>[0-9]+)$',
        nviews.edit, name="edit"),
    url(r'^report/(?P<model_name>[A-Za-z]+)/(?P<id>[0-9]+)$', nviews.report,
        name="new_report"),
    url(r'^resolve_report/(?P<report_id>[0-9]+)$', nviews.resolve_report,
        name="resolve_report"),

    url(r'account/?$', accviews.register, name="register_ajax"),
]

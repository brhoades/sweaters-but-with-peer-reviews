from django.conf.urls import url
import browse.views as bviews

urlpatterns = [
    url(r'^user/(?P<id>[0-9]+)?$', bviews.profile, name="profile"),
    url(r'^user/?$', bviews.setting, name="setting"),
    url(r'^user/wardrobe/?$', bviews.wardrobe, name="wardrobe"),

    url(r'^school/(?P<school_id>[0-9]+)?$', bviews.school, name="school"),
    url(r'^schools/(?P<page>[0-9]+)?$', bviews.schools, name="schools"),

    url(r'^professors/(?P<page>[0-9]+)?$', bviews.professors,
        name="professors"),
    url(r'^professor/(?P<professor_id>[0-9]+)?$',
        bviews.professor, name="professor"),

    url(r'^review/(?P<review_id>[0-9]+)/?$', bviews.review, name="review"),
    url(r'^reviews/?$', bviews.reviews, name="reviews"),
    url(r'^reviews/(?P<page>[0-9]+)/?$', bviews.reviews, name="reviews"),
    url(r'^reviews/(?P<page>[0-9]+)/(?P<type>[A-Za-z_]+)/?$', bviews.reviews,
        name="reviews_by_type"),
    url(r'^reviews/(?P<page>[0-9]+)/(?P<type>[A-Za-z_]+)/'
        '(?P<first_id>[0-9]+)/?$', bviews.reviews, name="reviews_by_type_one"),
    url(r'^reviews/(?P<page>[0-9]+)/(?P<type>[A-Za-z_]+)/(?P<first_id>[0-9]+)'
        '/(?P<second_id>[0-9]+)/?$', bviews.reviews,
        name="reviews_by_type_two"),

    url(r'^peerreview/(?P<peerreview_id>[0-9]+)/?$', bviews.peer_review,
        name="peer_review"),

    url(r'logout/?$', bviews.logout, name="logout"),

    url(r'^sandbox/?$', bviews.sandbox, name="sandbox")
]

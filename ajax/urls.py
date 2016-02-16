from django.conf.urls import url
import ajax.views as aviews

urlpatterns = [
    url(r'^professors?$', aviews.get_professors),
    url(r'^courses?$', aviews.get_courses),
    url(r'^courses_matching/(?P<partial>.+)$',
        aviews.get_courses_matching),
    url(r'^professors_matching/(?P<partial>.+)$',
        aviews.get_professors_matching),
    url(r'^course_per_professor$', aviews.get_course_per_professor),
]

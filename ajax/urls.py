from django.conf.urls import url
import ajax.views as aviews

urlpatterns = [
    url(r'^professors?$', aviews.get_professors),
    url(r'^courses?$', aviews.get_courses),
    url(r'^course_per_professor?$', aviews.get_course_per_professor),
]

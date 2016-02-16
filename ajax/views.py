from browse.models import Professor, Course
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q


def get_professors(request):
    return HttpResponse(serializers.serialize("json", Professor.objects.all()))


def get_courses(request):
    return HttpResponse(serializers.serialize("json", Course.objects.all()))


def get_courses_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        Course.objects.filter(name__contains=partial)))


def get_professors_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        Professor.objects
                        .filter(Q(last_name__contains=partial)
                                | Q(first_name__contains=partial))))


def get_course_per_professor(request):
    # for prof in Professor.objects:
    # FIXME: courses and professors aren't related
    return HttpResponse(serializers.serialize("json", Course.objects.all()))

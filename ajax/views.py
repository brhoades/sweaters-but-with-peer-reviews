from browse.models import Professor, Course, School, Department
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q


def get_professors(request):
    return HttpResponse(serializers.serialize("json", Professor.objects.all()))


def get_courses(request):
    return HttpResponse(serializers.serialize("json", Course.objects.all()))


def get_courses_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        Course.objects.filter(name__icontains=partial)))


def get_schools_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        School.objects.filter(name__icontains=partial)))


def get_departments_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        Department.objects.filter(name__icontains=partial)))


def get_professors_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        Professor.objects
                        .filter(Q(last_name__icontains=partial)
                                | Q(first_name__icontains=partial))))


def get_course_per_professor(request):
    # for prof in Professor.objects:
    # FIXME: courses and professors aren't related
    return HttpResponse(serializers.serialize("json", Course.objects.all()))

from browse.models import Review, Professor, Course, School, Department
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q

import json


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


def get_fields_for_model(request, model=""):
    # Create modelmap
    modelmap = {}
    models = [Review, Professor, Course, School, Department]

    for m in models:
        modelmap[m.__name__] = m
        modelmap[m.__name__.lower()] = m

    if model not in modelmap:
        return HttpResponse(json.dumps({"error": "Unknown model requested."}))

    # Create list of fields
    fields = []
    print(modelmap[model])
    for field in modelmap[model]._meta.fields:
        # Ignore automatically created fields
        if not field.auto_created and "auto_now" not in field.__dict__:
            if field.column.endswith("_id"):
                fields.append(field.column[:-3])
            else:
                fields.append(field.column)

    return HttpResponse(json.dumps(fields))


def get_course_per_professor(request):
    # for prof in Professor.objects:
    # FIXME: courses and professors aren't related
    return HttpResponse(serializers.serialize("json", Course.objects.all()))

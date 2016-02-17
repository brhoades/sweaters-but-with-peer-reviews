from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.core.urlresolvers import reverse

import json

from new.views import json_error
from browse.models import Review, Professor, School, Department, Course, \
    Field, FieldCategory
from new.forms import ReviewForm, ProfessorForm, SchoolForm, DepartmentForm, \
    FieldForm, FieldCategoryForm, CourseForm


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


def get_fields_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        Field.objects.filter(name__icontains=partial)))


def get_fields_categories_matching(request, partial):
    return HttpResponse(serializers.serialize("json",
                        FieldCategory.objects.filter(name__icontains=partial)))


def get_form_from_model(model):
    """
    Returns an array of fields which must be filled. Raises ValueError
    if unknown model is passed.
    """
    modelforms = [ReviewForm, ProfessorForm, CourseForm, SchoolForm,
                  DepartmentForm, FieldForm, FieldCategoryForm]

    for form in modelforms:
        if form.Meta.model is model:
            return form
    else:
        raise ValueError("Unknown model passed.")


def get_model_from_string(model):
    modelmap = {}
    models = [Review, Professor, Course, School, Department, Field,
              FieldCategory]

    for m in models:
        modelmap[m.__name__] = m
        modelmap[m.__name__.lower()] = m

    if model not in modelmap:
        raise ValueError("Unknown model string provided.")

    return modelmap[model]


def get_fields_for_model(request, model=""):
    try:
        # Create modelmap
        model = get_model_from_string(model)
    except ValueError:
        return HttpResponse(json.dumps({"error":
                                        {"error":
                                         "Unknown model requested."}}))

    # Create list of fields
    """
    fields = []
    for field in model._meta.fields:
        # Ignore automatically created fields
        if not field.auto_created and "auto_now" not in field.__dict__:
            if field.column.endswith("_id"):
                fields.append(field.column[:-3])
            else:
                fields.append(field.column)
    """
    return HttpResponse(json.dumps(get_form_from_model(model).Meta.fields))


def get_course_per_professor(request):
    # for prof in Professor.objects:
    # FIXME: courses and professors aren't related
    return HttpResponse(serializers.serialize("json", Course.objects.all()))


def get_view_for_model(request, model="", id=-1):
    # Map for model to page names
    model_map = {"review": Review,
                 "professor": Professor,
                 "school": School,
                 }

    if model not in model_map:
        json_error("Unknown/unsupported model specified")

    return HttpResponse(json.dumps({"url": reverse(model, args=[id])}))

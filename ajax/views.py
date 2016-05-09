from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse

import json

from new.views import json_error
from browse.models import Review, Professor, School, Department, Course, \
    Field, FieldCategory
from new.utils import get_model_from_string, get_form_from_model


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
    # Smash in school names too
    depts = Department.objects.filter(name__icontains=partial)
    return HttpResponse(json.dumps([x.to_json() for x in depts]))


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

    # This one is sort of hacked in, it redirects to your reports list
    if model == "resolve_report":
        url = "/browse/reports"
    else:
        url = reverse(model, args=[id])

    return HttpResponse(json.dumps({"url": url}))


def login(request):
    """
    Our view for logging in.
    """
    response = {"refresh": False, "message": "Unknown communication method"}

    if request.method == 'POST':
        data = json.loads(request.body.decode())
        if "username" not in data:
            response["message"] = "Missing username"
        elif "password" not in data:
            response["message"] = "Missing password"
        else:
            username = data["username"]
            password = data["password"]

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    response["message"] = ""
                    response["refresh"] = True
                else:
                    response["message"] = "Your account is disabled."
            else:
                response["message"] = "Invalid login details."

    return JsonResponse(response)


def model_values(request, model_name, id):
    """
    Gets values for a model instance.
    """
    try:
        # Create modelmap
        model = get_model_from_string(model_name)
    except ValueError:
        return HttpResponse(json.dumps({"error":
                                        {"error":
                                         "Unknown model requested."}}))

    instance = model.objects.filter(id=id)[0]

    if not instance:
        return json_error("Unknown id provided.")

    return HttpResponse(instance.to_json())


def get_fields_for_model(request, model=""):
    try:
        form = get_form_from_model(model)
    except ValueError:
        return HttpResponse(json.dumps({"error":
                                        {"error":
                                         "Unknown model requested."}}))

    fields = form.Meta.fields[:]
    fields.extend(form.Meta.fields_extra)

    return HttpResponse(json.dumps(fields))

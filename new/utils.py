from django.http import HttpResponse
from django.template import loader, RequestContext

from browse.models import Review, Professor, School, Department, \
    Field, FieldCategory, Course, ReviewComment, Report
from new.forms import ReviewForm, ProfessorForm, SchoolForm, DepartmentForm, \
    FieldForm, FieldCategoryForm, CourseForm, CommentForm, ReportForm

import json

MODEL_MAP = {"review": Review,
             "professor": Professor,
             "school": School,
             "department": Department,
             "course": Course,
             "field": Field,
             "fieldcategory": FieldCategory,
             "reviewcomment": ReviewComment,
             "report": Report,
             }

MODEL_FORM_MAP = {"review": ReviewForm,
                  "professor": ProfessorForm,
                  "school": SchoolForm,
                  "course": CourseForm,
                  "department": DepartmentForm,
                  "field": FieldForm,
                  "fieldcategory": FieldCategoryForm,
                  "reviewcomment": CommentForm,
                  "report": ReportForm
                  }


def json_error(data):
    return HttpResponse(json.dumps({"error": data}))


def check_fields_in_data(data, model, form):
    """
    Go through every key in data. Check that, for a given model, there are
    all required keys. Check that each key, if it's a foreign key, points
    to a valid object. It returns a json error if invalid, None otherwise.
    """
    response = {"error": {"error": ""}}

    if "error" in data:
        del data["error"]

    for key in data.keys():
        # Check that this is a key that exists
        if (key not in model._meta.get_all_field_names() and
                key not in form.Meta.fields_extra):
            return json_error({"error": ''.join(["No field for ",
                                                 str(model), ": \"",
                                                 key, "\""])})
        # Check that an id field exists for required foreign key fields
        field = model._meta.get_field(key)
        if field.is_relation and isinstance(data[key], dict):
            if "id" not in data[key]:
                response["error"][key] = "No {} specified".format(
                    field.target_field.model.__name__)
            elif not field.target_field.model.objects.filter(
                    id=data[key]["id"]).count():
                response["error"][key] = "{} does not exist".format(
                    field.target_field.model.__name__)
            else:
                data[key] = field.target_field.model.objects.get(
                    id=data[key]["id"])

    # Check for required keys
    for field in model.Meta.fields[:].extend(model.Meta.fields_extra):
        if field not in data or data[field] == "" and field != "location":
            response["error"][field] = "No {} specified".format(
                field)


def get_template_for_model(request, model_form_map, page):
    template = None
    context = RequestContext(request)

    if page == "review":
        template = loader.get_template("new/review.html")
    elif page == "professor":
        template = loader.get_template("new/professor.html")
    elif page == "school":
        template = loader.get_template("new/school.html")
    elif page == "department":
        template = loader.get_template("new/department.html")
    elif page == "course":
        template = loader.get_template("new/course.html")
    elif page == "field":
        template = loader.get_template("new/field.html")
    elif page == "fieldcategory":
        template = loader.get_template("new/fieldcategory.html")
    elif page == "report":
        template = loader.get_template("new/report.html")
    else:
        return HttpResponse("Put a 404 here or something.")

    context["form"] = MODEL_FORM_MAP[page]
    return HttpResponse(template.render(context))


def get_form_from_model(model):
    if model not in MODEL_FORM_MAP:
        raise ValueError("Unknown model {}".format(model))
    return MODEL_FORM_MAP[model]


def get_model_from_string(model):
    return MODEL_MAP[model]

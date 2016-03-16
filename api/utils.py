from django.http import HttpResponse
from django.template import RequestContext, loader

import json


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
    else:
        return HttpResponse("Put a 404 here or something.")

    context["form"] = model_form_map[page]
    return HttpResponse(template.render(context))


def json_error(data):
    return HttpResponse(json.dumps({"error": data}))

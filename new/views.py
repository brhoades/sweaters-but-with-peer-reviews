from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext

import json

from browse.models import ReviewVote, Review, Professor, School, Department, \
    Field, FieldCategory
from new.forms import ReviewForm, ProfessorForm, SchoolForm, DepartmentForm, \
    FieldForm, FieldCategoryForm


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


@login_required
def new(request, page=None):
    model = None
    response = {"error": {"error": ""}}
    model_map = {"review": Review,
                 "professor": Professor,
                 "school": School,
                 "department": Department,
                 "field": Field,
                 "fieldcategory": FieldCategory,
                 }
    model_form_map = {"review": ReviewForm,
                      "professor": ProfessorForm,
                      "school": SchoolForm,
                      "department": DepartmentForm,
                      "field": FieldForm,
                      "fieldcategory": FieldCategoryForm,
                      }

    if request.method != "POST":
        return get_template_for_model(request, model_form_map, page)

    data = json.loads(request.body.decode())

    if page not in model_map.keys():
        return json_error({"error": "Unknown page requested."})

    model = model_map[page]

    # Otherwise we will complain about it existing
    del data["error"]

    # If model has an owner or created by field, add us
    if model_form_map[page].needs_owner:
        data["owner"] = request.user
    elif model_form_map[page].needs_created_by:
        data["created_by"] = request.user

    for key in data.keys():
        # Check that this is a key that exists
        if key not in model._meta.get_all_field_names():
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
    for field in model_form_map[page].Meta.fields:
        if field not in data or data[field] == "":
            response["error"][field] = "No {} specified".format(
                field)

    # Look for any errors
    for k, v in response["error"].items():
        if len(v) > 0:
            return HttpResponse(json.dumps(response))

    # Try to create it
    try:
        new = model(**data)
    except Exception as e:
        print("ERROR: " + str(e))
        return HttpResponse(json_error({"error": str(e)}))

    # Save and return all info
    new.save()
    return HttpResponse(json.dumps({"id": new.id, "error": {}}))


def addVote(request):
    if request.method == "POST":
        if not request.user.is_authenticated():
            jsonResponse = {"success": False,
                            "error": "User not logged in"}
            return HttpResponse(json.dumps(jsonResponse),
                                content_type="application/json")

        review_id = request.POST.get("review-id")
        action = request.POST.get("action").lower()
        user = request.user
        review = Review.objects.get(id=review_id)

        try:
            exists = ReviewVote.objects.filter(target=review,
                                               owner=user).exists()

            # vote doesn't exist yet, and a vote direction is given
            if not exists and (action == "up" or action == "down"):
                vote = ReviewVote(target=review,
                                  owner=user,
                                  quality=(action == "up"))
                vote.save()
            # vote does exist and needs to be removed
            elif exists:
                vote = ReviewVote.objects.get(target=review, owner=user)
                # This only deletes the vote if the action is
                # opposite the current vote
                if (action != "up" and vote.quality) or \
                        (action != "down" and not vote.quality):
                    vote.delete()

        except:
            jsonResponse = {"success": False,
                            "error": "Could not complete vote"}
            return HttpResponse(json.dumps(jsonResponse),
                                content_type="application/json")

    return HttpResponse(json.dumps({"success": True}),
                        content_type="application/json")

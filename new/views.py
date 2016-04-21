from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext

from new.utils import json_error, check_fields_in_data, MODEL_MAP, \
    MODEL_FORM_MAP
from browse.models import ReviewVote, Report, Review

import json
import datetime


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

    context["form"] = MODEL_FORM_MAP[page]
    return HttpResponse(template.render(context))


@login_required
def edit(request, page=None, id=None):
    # Check that id exists for page.
    if page not in MODEL_MAP.keys():
        return json_error({"error": "Unknown page requested."})

    instances = MODEL_MAP[page].objects.filter(id=id)
    if len(instances) != 1:
        return json_error({"error": "Unknown {} id {} provided."
                                    .format(page, id)})

    owner = None
    instance = instances[0]
    if hasattr(instance, "created_by"):
        owner = instance.created_by
    elif hasattr(instance, "owner"):
        owner = instance.owner

    if owner and owner != request.user:
        return json_error({"error": "You do not own this instance."})

    # Functionality is so similar to new, just hand it off
    return new(request, page=page, id=id, type="edit")


def new(request, type="new", page=None, id=None):
    if not request.user.is_authenticated():
        return json_error({"error": "Please login to add a {}.".format(page)})

    model = None
    response = {"error": {"error": ""}}
    model_map = MODEL_MAP

    if request.method != "POST":
        return get_template_for_model(request, MODEL_FORM_MAP, page)

    data = json.loads(request.body.decode())

    if page not in model_map.keys():
        return json_error({"error": "Unknown page requested."})

    model = model_map[page]

    # If model has an owner or created by field, add us
    if MODEL_FORM_MAP[page].needs_owner:
        data["owner"] = request.user
    elif MODEL_FORM_MAP[page].needs_created_by:
        data["created_by"] = request.user

    # FIXME: Is this necessary? It seems like it should autoresolve this
    if page == "reviewcomment":
        data["target"] = Review.objects.get(id=int(data["target"]))

    res = check_fields_in_data(data, model)
    if res:
        return res

    # Look for any errors
    for k, v in response["error"].items():
        if len(v) > 0:
            return HttpResponse(json.dumps(response))
    try:
        if type == "new":
            # Try to create it
            new = model(**data)
        elif type == "edit":
            # We can assume it exists
            new = model.objects.get(id=id)
            for k, v in data.items():
                setattr(new, k, data[k])
            if hasattr(new, "updated_ts"):
                new.updated_ts = datetime.datetime.now()
    except Exception as e:
        print("ERROR: " + str(e))
        return HttpResponse(json_error({"error": str(e)}))

    for field in MODEL_FORM_MAP[page].Meta.fields:
        response["error"][field] = ""  # clear errors

    new.save()
    response["id"] = new.id  # return new id at top level.
    # Save and return all info

    return HttpResponse(json.dumps(response))


def addVote(request, wat=None):
    # I don't know where 'wat' is coming from, but it's not needed...
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
            vote = ReviewVote.objects.filter(target=review,
                                             owner=user)

            # If the vote exists, we need to change it based on input.
            # Currently votes are changed as such:
            #     If the user presses the same direction as their current vote
            #     then the vote is removed
            #     If the user presses opposite their vote, the vote is changed
            #     to the new direction
            if vote.exists():
                vote = vote[0]
                if (vote.quality and action == "up") or \
                   (not vote.quality and action == "down"):
                    vote.delete()
                else:
                    vote.quality = (action == "up")
                    vote.save()
            # vote doesn't exist yet, then it needs to be created.
            elif (action == "up" or action == "down"):
                vote = ReviewVote(target=review,
                                  owner=user,
                                  quality=(action == "up"))
                vote.save()

        except:
            jsonResponse = {"success": False,
                            "error": "Could not complete vote"}
            return HttpResponse(json.dumps(jsonResponse),
                                content_type="application/json")

        return HttpResponse(json.dumps({"success": True}),
                            content_type="application/json")
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def report(request, model_name, id):
    if request.method == "POST":
        res = {}
        if model_name not in MODEL_MAP.keys():
            return HttpResponse(json.dumps({"error": "Unknown model."}),
                                content_type="application/json")

        model = MODEL_MAP[model_name]
        template = loader.get_template("new/report.html")
        data = json.loads(request.body.decode())

        # FIXME: flip shit if this isn't here.
        inst = MODEL_MAP[model_name].objects.get(id=id)

        res = check_fields_in_data(data, Report)
        if res:
            return res

        # FIXME handle shit that doesn't exist (ie report for bad instance)
        Report.create(model, id, request.user, data["comment"])
        context = {"instance": inst, "model": model_name}

        return HttpResponse(template.render(context))
    else:
        if model_name not in MODEL_MAP.keys():
            return HttpResponse("Put a 404 here or something.")

        inst = MODEL_MAP[model_name].objects.get(id=id)
        template = loader.get_template("new/report.html")
        context = {"instance": inst, "model": model_name, "id": id}

        return HttpResponse(template.render(context))

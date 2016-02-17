from django.http import HttpResponse
from browse.models import ReviewVote, Review, Professor
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext
import json


def get_template_for_model(request, page):
    template = None
    context = RequestContext(request)

    if page == "review":
        template = loader.get_teamplate("new/review.html")
    elif page == "professor":
        template = loader.get_template("new/professor.html")
    else:
        return HttpResponse("Put a 404 here or something.")

    return HttpResponse(template.render(context))


def json_error(data):
    return HttpResponse(json.dumps({"error": data}))


@login_required
def new(request, page=None):
    model = None
    response = {"error": {}}
    model_map = {"review": Review,
                 "professor": Professor
                 }

    if request.method != "POST":
        return get_template_for_model(request, page)

    data = json.loads(request.body.decode())

    if page not in model_map.keys():
        return json_error("Unknown page requested.")

    model = model_map[page]

    for key in data.keys():
        # Check that this is a key that exists
        if key not in model._meta.get_all_field_names():
            return json_error(''.join(["No field for ", str(model), ": ",
                                       key]))
        # Check that an id field exists for required foreign key fields
        field = model._meta.get_field(key)
        if field.get_internal_name() == "ForeignKey":
            if "id" not in data[key]:
                response["error"][key] = "No {} specified".format(
                    field.target_field.model.__name__)
            elif not model.objects.exists(id=data[key]["id"]):
                response["error"][key] = "{} does not exist".format(
                    field.target_field.model.__name__)

    # Look for any errors
    for k, v in response["error"].items():
        if len(v) > 0:
            return HttpResponse(json.dumps(response))

    # If model has an owner or created by field, add us
    if "owner" in model.get_all_field_names():
        data["owner"] = request.user
    elif "created_by" in model.get_all_field_names():
        data["created_by"] = request.user

    # Try to create it
    try:
        new = model(**data)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    # Save and return all info
    new.save()
    return HttpResponse(json.dumps({"success": True,
                                    "new": new
                                    }))


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

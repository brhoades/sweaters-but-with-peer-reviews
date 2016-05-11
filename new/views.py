from django.http import HttpResponse, HttpResponseNotAllowed, \
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from new.utils import json_error, check_fields_in_data, MODEL_MAP, \
    MODEL_FORM_MAP, get_template_for_model
from browse.models import ReviewVote, Report, Review

import json
import datetime
import tempfile


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
        if request.method == "POST":
            return json_error({"error": "Please login to add a {}."
                                        .format(page)})
        else:
            redir = request.META.get("HTTP_REFERER")
            if not redir:
                redir = reverse("home")
            messages.error(request,
                           "You must be logged in to add a {}.".format(page))
            return HttpResponseRedirect(redir)

    model = None
    response = {"error": {"error": ""}}

    if request.method != "POST":
        return get_template_for_model(request, MODEL_FORM_MAP, page)

    data = json.loads(request.body.decode())

    if page not in MODEL_MAP:
        return json_error({"error": "Requested page type \"{}\" does not have"
                                    " a known model.".format(page)})
    if page not in MODEL_FORM_MAP.keys():
        return json_error({"error": "Requested page type \"{}\" does not have"
                                    " a known form.".format(page)})

    model = MODEL_MAP[page]
    form = MODEL_FORM_MAP[page]

    # If model has an owner or created by field, add us
    if form.needs_owner:
        data["owner"] = request.user
    elif form.needs_created_by:
        data["created_by"] = request.user

    # FIXME: Is this necessary? It seems like it should autoresolve this
    if page == "reviewcomment":
        data["target"] = Review.objects.get(id=int(data["target"]))

    # Check for files, in this case it's avatar if ever
    if "avatar" in data:
        fn = None
        res = {}
        try:
            # Write into tempfile
            fn = tempfile.NamedTemporaryFile()
            with open(fn, mode="w") as fh:
                fh.write(data["avatar"].decode("base64"))
        except Exception as e:
            res["error"] = "Provided image did not decode from base64 properly"
            return HttpResponse(json.dumps(res))
        res["avatar"] = fn

    res = check_fields_in_data(data, model, form)
    if res:
        return res

    # Look for any errors
    for k, v in response["error"].items():
        if len(v) > 0:
            return HttpResponse(json.dumps(response))
    try:
        emptyKeys = []
        for key, value in data.items():
            if value == '':
                emptyKeys.append(key)
        for key in emptyKeys:
            data.pop(key)

        print(data)
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

        new.full_clean()
    except ValidationError as e:
        print("ERROR: " + str(e))
        errorDict = {}
        for key, value in e.message_dict.items():
            if isinstance(value, list):
                errorDict[key] = " ".join(value).strip("[]/'")

        return HttpResponse(json_error(errorDict))

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
    """
    This view serves both the proper form page and the POST requests for
    the report form page.

    It's essentially a clone of new but with a few fixes since the model is
    mucked up with metamadness.
    """
    if model_name not in MODEL_MAP:
        if request.method != "POST":
            return HttpResponse("Unknown model name specified.")
        return json_error({"error": "Requested page type \"{}\" does not "
                                    "have a known model."
                                    .format(model_name)
                           })
    if model_name not in MODEL_FORM_MAP:
        if request.method != "POST":
            return HttpResponse("Unknown model name specified.")
        return json_error({"error": "Requested page type \"{}\" does not "
                                    "have a known form.".format(model_name)
                           })

    if request.method == "POST":
        res = {}
        data = json.loads(request.body.decode())

        target_model = MODEL_MAP[model_name]
        form = MODEL_FORM_MAP["report"]

        inst = target_model.objects.get(id=id)
        if not inst:
            json_error({"error": "Unknown model instance id for provided model"
                                 " ({} for '{}').".format(id, model_name)})

        err = check_fields_in_data(data, Report, form)
        if err:
            return err

        print(data)

        new = Report.create(target_model, id, request.user, data["summary"],
                            data["text"])
        new.save()
        res["id"] = new.id

        return HttpResponse(json.dumps(res),
                            content_type="application/json")
    else:
        inst = MODEL_MAP[model_name].objects.get(id=id)
        template = loader.get_template("new/report.html")
        context = {"instance": inst, "model": model_name, "id": id}

        return HttpResponse(template.render(context))


@login_required
def resolve_report(request, report_id):
    """
    This view serves both the proper form page and the POST requests for
    the resolve report form page.

    It's essentially a clone of report but with a few changes to make
    resolution better.
    """
    # TODO: Check if staff
    inst = Report.objects.get(id=report_id)
    if not inst:
        return json_error({"error": "Unknown report with id {}".format(id)})

    if inst.handled:
        return json_error({"error": "Report has already been resolved."})

    if request.method == "POST":
        res = {}
        data = json.loads(request.body.decode())

        if "text" not in data:
            return json_error({"text": "Missing text field."})

        if "summary" not in data or data["summary"] == "":
            return json_error({"summary": "Missing action field."})

        inst.resolve(by=request.user, comment=data["text"])
        res["id"] = inst.id

        return HttpResponse(json.dumps(res),
                            content_type="application/json")
    else:
        template = loader.get_template("new/resolve_report.html")
        context = {"instance": inst, "id": report_id}

        return HttpResponse(template.render(context))

from django.http import HttpResponse
from browse.models import ReviewVote, Review
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import json


@login_required
def new(request, page=None):
    # context = RequestContext(request)
    data = json.loads(request.body.decode())
    new = None
    response = {"error":
                {
                    "error": "",
                    "text": "",
                    "target": "",
                    "course": ""
                }
                }

    if "target" not in data or "id" not in data["target"]:
        response["error"]["target"] = "No professor specified"
    if "course" not in data or "id" not in data["course"]:
        response["error"]["course"] = "No course specified"
    if "text" not in data or len(data["text"]) < 50:
        response["error"]["text"] = "Review is not long enough."

    # Look for any errors
    for k, v in response["error"].items():
        if len(v) > 0:
            return HttpResponse(json.dumps(response))
    try:
        new = Review(target_id=data["target"]["id"],
                     course_id=data["course"]["id"],
                     text=data["text"],
                     owner=request.user)
    except Exception as e:
        return HttpResponse(json.dumps({"error": str(e)}))

    new.save()
    return HttpResponse(json.dumps(
        {"redirect": reverse('review', kwargs={"review_id": new.id})}))


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

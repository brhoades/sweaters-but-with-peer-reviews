from django.http import HttpResponse, HttpResponseNotAllowed
from browse.models import ReviewVote, Review
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

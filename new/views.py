from django.shortcuts import render
from django.http import HttpResponse
from new.forms import ReviewForm, CourseForm, ProfessorForm
from browse.models import ReviewVote, Review
import json


def new(request, page=None):
    template = "new/index.html"
    context = {}

    return render(request, template, context)


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

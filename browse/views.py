from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from browse.models import Review, User, Professor, School, Course,\
    ReviewComment, Report, PeerReview, Log
from django.contrib.auth import logout as auth_logout
from browse.get_utils import _get_all_review_votes, paginate
from new.forms import PeerReviewForm, SchoolForm
from chartit import DataPool, Chart
import json
from new.views import MODEL_MAP


def index(request, message=""):
    template = "browse/index.html"

    context = RequestContext(request)

    context["review_votes"] = _get_all_review_votes(request)[0:5]

    return render(request, template, context)


def profile(request, id=None, page=0):
    """
    This is our profile page. It's passed, optionally, a user id as "id" in
    kwargs. If it gets an id, it spits out a profile. If it doesn't, it spits
    out a listing of all users with links to profiles.

    If a page is provided, it skips forward that page * items per page.
    """
    template = "browse/profile.html"
    context = RequestContext(request)

    # Specific profile was requested
    if id is not None:
        # Could use 404 shortcut, or a simple redirect for invalid user id's
        context["profile"] = get_object_or_404(User, id=id)
    # User logged in and should see own profile
    elif request.user.is_authenticated():
        context["profile"] = request.user
    # No Profile specified and user is not logged in
    else:
        # One option is redirect as such.
        messages.info(request, "Please login to view your profile.")
        return redirect("home")

    context["review_votes"] = _get_all_review_votes(
        request,
        {"owner": context["profile"].id})

    voteCount = 0
    for review, v in context["review_votes"]:
        votes = review.reviewvote_set.all()
        voteCount += sum([1 if vote.quality else -1 for vote in votes])

    context["user_rating"] = voteCount

    return render(request, template, context)


def setting(request, id=None, page=0):
    """
    Settings stuff goes here, like messing with first names last names, etc.
    It should display the data of the user unless they are not logged in.
    """
    template = "browse/setting.html"
    context = RequestContext(request)

    # Specific profile was requested
    if id is not None:
        # Could use 404 shortcut, or a simple redirect for invalid user id's
        context["profile"] = get_object_or_404(User, id=id)
    # User logged in and should see own profile
    elif request.user.is_authenticated():
        context["profile"] = request.user
    # No Profile specified and user is not logged in
    else:
        # One option is redirect as such.
        messages.info(request, "Please login to view your profile.")
        return redirect("home")

    userReviews = context["profile"].review_set.all()

    voteCount = 0
    for review in userReviews:
        votes = review.reviewvote_set.all()
        voteCount += sum([1 if vote.quality else -1 for vote in votes])

    context["user_rating"] = voteCount

    return render(request, template, context)


def schools(request, page):
    template = loader.get_template("browse/schools.html")
    context = RequestContext(request)
    context["schoolForm"] = SchoolForm()

    # Get our page numbers to display, our page, all objects, and the
    # range of that all we're going to send back.
    context["pages"], context["page"], all, start, end = paginate(page, School)
    context["schools"] = all[start:end]

    return HttpResponse(template.render(context))


def school(request, school_id=None, page=0):
    """
    This is a school page. If no id is provided, it displays a listing of
    all schoosl with information about each. If one is provided, it provides
    an overview about that school.

    If a page is provided, it skips forward that page * items per page.
    """
    template = loader.get_template("browse/school.html")
    context = RequestContext(request)

    context["school"] = get_object_or_404(School, id=school_id)

    context["school_location"] = context["school"].human_location

    # FIXME: Paginate
    context["review_votes"] = \
        _get_all_review_votes(request, {"target__school_id": school_id})[0:5]

    context["courses"] = Course.objects.filter(
        department__school__id=school_id)

    context["professors"] = Professor.objects.filter(school_id=school_id)

    return HttpResponse(template.render(context))


def professors(request, page):
    template = loader.get_template("browse/professors.html")
    context = RequestContext(request)
    context["schoolForm"] = SchoolForm()

    professors = []
    context["professors"] = professors
    context["pages"], context["page"], all, start, end = paginate(page,
                                                                  Professor)

    for p in Professor.objects.order_by('-created_ts')[start:end]:
        professors.append(p)

    return HttpResponse(template.render(context))


def professor(request, professor_id=None, page=0):
    """
    This is a professor profile page (not a user). It provides information
    about courses taught, latest reviews, and aggregate ratings. If an id is
    not specified, it provides a listing of all professors (paginated).

    If a page is provided, it skips forward that page * items per page.
    """
    template = loader.get_template("browse/professor.html")
    context = RequestContext(request)

    context["professor"] = get_object_or_404(Professor, id=professor_id)

    # FIXME: Paginate
    context["review_votes"] = _get_all_review_votes(request,
                                                    {"target": professor_id})
    context["courses"] = []
    courses = (Review.objects.filter(target_id=professor_id).values("course")
               .distinct())

    for course in courses:
        context["courses"].append(Course.objects.get(id=course["course"]))

    context["schools"] = [course.department.school for course
                          in context["courses"]]

    reviewdata = (Review.objects.filter(target_id=professor_id))
    profdata = DataPool(series=[{'options': {'source': reviewdata}, 'terms':
                                 ['id', 'rating_value', 'rating_difficulty',
                                 'rating_overall']}])

    chart = Chart(datasource=profdata, series_options=[{'options':
                                                        {'type': 'line',
                                                         'stacking': False},
                                                        'terms':
                                                        {'id':
                                                         ['rating_value',
                                                          'rating_difficulty',
                                                          'rating_overall']}}],
                  chart_options={'title': {'text': 'Ratings of Professor'},
                                 'xAxis': {'title': {'text': 'Reviews'},
                                           'ceiling': 25},
                                 'yAxis': {'title': {'text': 'Ratings'},
                                           'floor': 0, 'ceiling': 5}})

    context["chart"] = chart

    return HttpResponse(template.render(context))


def review(request, review_id=0):
    """
    View a single review given an ID.
    """
    template = loader.get_template("browse/review.html")
    context = RequestContext(request)

    context["review"] = get_object_or_404(Review, id=review_id)
    context["comments"] = ReviewComment.objects.filter(target_id=review_id)\
                                               .order_by("created_ts")

    return HttpResponse(template.render(context))


def reviews(request, type="all", first_id=None, second_id=None, page=1):
    """
    This is the general-purpose review-viewing page. It allows for returning
    views of specific requests from the user.

    :Parameters:
        * *page*: (``int``) --
            The page to start listing from.
        * *type*: (``str``) --
            The type of review view page to get. Valid types are:
                * all (default)
                * by_school
                * by_professor
                * by_school_professor
        * *first_id*: (``int``) --
            The first id of the requested view type (ie professor).
        * *second_id*: (``int``) --
            The second id of the requested view type (ie school).
    """
    template = "browse/reviews.html"
    context = RequestContext(request)
    context["pages"], context["page"], all, start, end = paginate(page, Review)
    context["review_votes"] = _get_all_review_votes(request)[start:end]
    context["schoolForm"] = SchoolForm()

    if type == "by_school":
        context["message"] =\
            "This is the page that lists all reviews for school {1}"\
            "(pg {0}).".format(page, first_id)
    elif type == "by_professor":
        context["message"] =\
            "This is the page that lists all reviews for professor"\
            " {1} (pg {0}).".format(page, first_id)

    elif type == "by_school_professor":
        context["message"] =\
            "This is the page for reviews of professor {1} from "\
            "school {0} (pg {2})."\
            .format(first_id, second_id, page)
    else:
        context["message"] =\
            "This is the page that lists all reviews (pg {0})."\
            .format(page)
    return render(request, template, context)


def report(request, report_id=None, page=0):
    template = loader.get_template("browse/report.html")
    context = RequestContext(request)

    context["report"] = get_object_or_404(Report, id=report_id)

    return HttpResponse(template.render(context))


def logout(request):
    """
    Our view for logging out.
    """
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def sandbox(request):
    """
    A place where we can test out different things for the site
    """
    template = "browse/sandbox.html"
    return render(request, template)


def delete(request):
    if request.method == "POST":
        if not request.user.is_authenticated():
            jsonResponse = {"success": False,
                            "error": "User is not logged in"}
            return HttpResponse(json.dumps(jsonResponse),
                                content_type="application/json")

        model_id = request.POST.get("model-id")
        model = request.POST.get("model").lower()
        user = request.user

        obj = MODEL_MAP[model].objects.get(id=model_id)

        if not user.is_superuser:
            if model in ["school", "professor"]:
                jsonResponse = {"success": False,
                                "error": model.capitalize() +
                                " cannot be deleted by non-admins," +
                                " delete would cause more delete to cascade."}
                return HttpResponse(json.dumps(jsonResponse),
                                    content_type="application/json")

            if hasattr(MODEL_MAP[model], 'created_by'):
                created_by_key = 'created_by'
            elif hasattr(MODEL_MAP[model], 'owner'):
                created_by_key = 'owner'
            else:
                jsonResponse = {"success": False,
                                "error": model.capitalize() +
                                " does not have an owner"}
                return HttpResponse(json.dumps(jsonResponse),
                                    content_type="application/json")
            if user != getattr(obj, created_by_key):
                jsonResponse = {"success": False,
                                "error": "You don't own this "+model}
                return HttpResponse(json.dumps(jsonResponse),
                                    content_type="application/json")

        obj.delete()

        return HttpResponse(json.dumps({"success": True}),
                            content_type="application/json")
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def wardrobe(request):
    """
    The view for each user to view their peer reivews.
    """

    template = "browse/wardrobe.html"
    context = {}

    context["peerReviews"] = request.user.peerreview_set.all()\
                                    .order_by('-created_ts')

    return render(request, template, context)


def peer_review(request, peerreview_id):
    """
    The view for look at and fill-out peerReview forms.
    """
    template = "browse/peerreview.html"
    context = {}

    peerReview = get_object_or_404(PeerReview, id=peerreview_id)

    if request.method == "GET":
        form = PeerReviewForm(instance=peerReview)
    elif request.method == "POST":
        form = PeerReviewForm(request.POST, instance=peerReview)
        reviewEdit = form.save(commit=False)

        reviewEdit.is_finished = True
        reviewEdit.save()
    else:
        return HttpResponseNotAllowed(["POST", "GET"])

    context["form"] = form

    return render(request, template, context)


@login_required
def logs(request, page=0):
    """
    The view for listing all log entries.
    """
    template = "browse/logs.html"
    context = {}

    logs = []
    context["logs"] = logs
    context["pages"], context["page"], all, start, end \
        = paginate(page, Log, "-created_ts", 15)

    for p in Log.objects.order_by('-created_ts')[start:end]:
        logs.append(p)

    return render(request, template, context)


def reports(request, page):
    template = loader.get_template("browse/reports.html")
    context = RequestContext(request)

    reports = []
    context["reports"] = reports
    context["pages"], context["page"], all, start, end \
        = paginate(page, Report, "-target_log__created_ts")

    for p in Report.objects.order_by('-target_log__created_ts')[start:end]:
        reports.append(p)

    return HttpResponse(template.render(context))

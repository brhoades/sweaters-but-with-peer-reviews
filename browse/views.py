from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from browse.models import Review, User, Professor, School, Course
from django.contrib.auth import logout as auth_logout
from browse.get_utils import _get_all_review_votes


def index(request, message=""):
    template = "browse/index.html"

    if message:
        messages.info(request, message)

    context = RequestContext(request)
    context["messages"] = messages.get_messages(request)

    context["review_votes"] = _get_all_review_votes(request)

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
        return redirect("index")

    userReviews = context["profile"].review_set.all()

    voteCount = 0
    for review in userReviews:
        votes = review.reviewvote_set.all()
        voteCount += sum([1 if vote.quality else -1 for vote in votes])

    context["user_rating"] = voteCount

    return render(request, template, context)


def setting(request, id=None):
    """
    Settings stuff goes here, like messing with first names last names, etc.
    It should display the data of the user unless they are not logged in. 
    """
    template = "browse/setting.html"
    context = RequestContext(request)


    return render(request, template, context)


def schools(request):
    template = loader.get_template("browse/schools.html")
    context = RequestContext(request)

    # HTML passthrough has to be enabled in the template... this is serialized.
    schools = []
    context["schools"] = schools

    for sch in School.objects.order_by("-created_ts"):
        thisschool = {}
        thisschool["school"] = sch
        thisschool["num_professors"] = (Professor.objects
                                        .filter(school_id=sch.id).count)
        thisschool["num_reviews"] = (Review.objects
                                     .filter(target__school_id=sch.id).count)
        schools.append(thisschool)

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

    return HttpResponse(template.render(context))


def professors(request):
    template = loader.get_template("browse/professors.html")
    context = RequestContext(request)

    professors = []
    context["professors"] = professors

    for p in Professor.objects.order_by('-created_ts'):
        thisprof = {}
        thisprof["professor"] = p

        thisprof["num_reviews"] = Review.objects.filter(target_id=p.id).count()
        thisprof["num_courses"] = (Review.objects.filter(target_id=p.id)
                                   .values("course").distinct().count())
        # Choose a school by the one they have the most reviews for.
        thisprof["school"] = (Review.objects.filter(target_id=p.id)
                              .annotate(Count("course", distinct=True))
                              .order_by())
        r = (Review.objects.values("course").annotate(count=Count("course"))
             .order_by())
        if len(r) > 0:
            thisprof["school"] = (Course.objects.get(id=r[0]["course"])
                                  .department.school)
        else:
            thisprof["school"] = ""

        professors.append(thisprof)

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

    return HttpResponse(template.render(context))


def review(request, review_id=0):
    """
    View a single review given an ID.
    """
    template = loader.get_template("browse/review.html")
    context = RequestContext(request)

    context["review"] = get_object_or_404(Review, id=review_id)

    return HttpResponse(template.render(context))


def reviews(request, type="all", first_id=None, second_id=None, page=0):
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
    context["review_votes"] = _get_all_review_votes(request)

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


def logout(request):
    """
    Our view for logging out.
    """
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("index")


def sandbox(request):
    """
    A place where we can test out different things for the site
    """
    template = "browse/sandbox.html"
    return render(request, template)

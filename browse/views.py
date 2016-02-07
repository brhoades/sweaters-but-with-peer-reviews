from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ReviewForm

from browse.models import Review, User
from django.contrib.auth import authenticate, login as auth_login, \
        logout as auth_logout


def index(request):
    template = loader.get_template("browse/index.html")
    context = RequestContext(request)

    # HTML passthrough has to be enabled in the template... this is serialized.
    context["message"] = "<h3>Sam Sucks and Dzu Rocks</h3>"
    context["numbers"] = []

    context["reviews"] = Review.objects.order_by('-created_ts')

    for x in range(1, 101):
        if x % 15 == 0:
            context["numbers"].append("{0} fizzbuzz".format(x))
        elif x % 5 == 0:
            context["numbers"].append("{0} buzz".format(x))
        elif x % 3 == 0:
            context["numbers"].append("{0} fizz".format(x))

    return HttpResponse(template.render(context))


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
        # context["profile"] = User.objects.get(id=id)
    # User logged in and should see own profile
    elif request.user.is_authenticated():
        context["profile"] = request.user
    # No Profile specified and user is not logged in
    else:
        # One option is redirect as such.
        messages.info(request, "Please Login to view your profile.")
        return redirect("login")

    return render(request, template, context)


def school(request, id=None, page=0):
    """
    This is a school page. If no id is provided, it displays a listing of
    all schoosl with information about each. If one is provided, it provides
    an overview about that school.

    If a page is provided, it skips forward that page * items per page.
    """
    template = loader.get_template("browse/school.html")
    context = RequestContext(request)

    if id is None:
        context["message"] = "This is a school listing, since there's no id"
    else:
        context["message"] = "This is a school overview for school {0}"\
                             .format(id)
    return HttpResponse(template.render(context))


def professor(request, id=None, page=0):
    """
    This is a professor profile page (not a user). It provides information
    about courses taught, latest reviews, and aggregate ratings. If an id is
    not specified, it provides a listing of all professors (paginated).

    If a page is provided, it skips forward that page * items per page.
    """
    template = loader.get_template("browse/professor.html")
    context = RequestContext(request)

    if id is None:
        context["message"] =\
                   "This is a professor listing, since there's no id"
    else:
        context["message"] = "This is a professor overview for prof #{0}"\
                             .format(id)
    return HttpResponse(template.render(context))


def review(request, review_id=0):
    """
    View a single review given an ID.
    """
    template = loader.get_template("browse/review.html")
    # should massage more than this
    context = {"review": Review.objects.get(id=review_id)}
    print(context["review"].__dict__)

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

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            # Here we can change things in the model.
            # IE user who posted, time posted, etc..
            model_instance.save()
    else:
        form = ReviewForm()
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
    context["form"] = form
    return render(request, template, context)


def login(request, user=None):
    """
    Our view for logging in.
    """
    template = "browse/login.html"
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect("index")
            else:
                context["message"] = "Your account is disabled."
                return render(request, template, context)
        else:
            context["message"] = "Invalid login details supplied."
            return render(request, template, context)
    else:
        return render(request, template, context)


def logout(request):
    """
    Our view for logging out.
    """
    auth_logout(request)
    return redirect("index")

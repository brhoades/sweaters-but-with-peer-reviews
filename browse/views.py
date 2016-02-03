from django.template import RequestContext, loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template("browse/index.html")

    # HTML passthrough has to be enabled in the template... this is serialized.
    context = {"message": "<h3>Sam Sucks and Dzu Rocks</h3>"}
    context["numbers"] = []

    for x in range(1, 101):
        if x % 15 == 0:
            context["numbers"].append("{0} fizzbuzz".format(x))
        elif x % 5 == 0:
            context["numbers"].append("{0} buzz".format(x))
        elif x % 3 == 0:
            context["numbers"].append("{0} fizz".format(x))

    return HttpResponse(template.render(context))


def profile(request, id):
    template = loader.get_template("browse/index.html")

    # HTML passthrough has to be enabled in the template... this is serialized.
    context = {"message": "<h3>This is a profile page</h3>"}
    return HttpResponse(template.render(context))


def school(request, id):
    template = loader.get_template("browse/index.html")

    # HTML passthrough has to be enabled in the template... this is serialized.
    if id is None:
        context = {"message":
                   "This is a school listing, since there's no id"}
    else:
        context = {"message":
                   "This is a school overview for school {0}"
                   .format(id)}
    return HttpResponse(template.render(context))


def professor(request, id):
    template = loader.get_template("browse/index.html")

    # HTML passthrough has to be enabled in the template... this is serialized.
    if id is None:
        context = {"message":
                   "This is a professor listing, since there's no id"}
    else:
        context = {"message":
                   "This is a professor overview for prof #{0}"
                   .format(id)}
    return HttpResponse(template.render(context))


def review_overview(request):
    template = loader.get_template("browse/index.html")

    context = {"message":
               "This is a recent reviews list, since there's no id"}

    return HttpResponse(template.render(context))


def review(request, school_id, professor_id):
    template = loader.get_template("browse/index.html")

    # HTML passthrough has to be enabled in the template... this is serialized.
    context = {"message":
               "This is the page for reviews of professor {1} from school {0}"
               .format(school_id, professor_id)}
    return HttpResponse(template.render(context))

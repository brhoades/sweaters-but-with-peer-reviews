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
    pass


def school(request, id):
    pass


def professor(request, id):
    pass


def review_overview(request):
    pass


def review(request, id):
    pass


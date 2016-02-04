from django.shortcuts import render
from new.forms import ReviewForm, CourseForm, ProfessorForm


def new(request, page=None):
    template = "new/index.html"
    context = {}

    if page == "professor":
        form = ProfessorForm()
    elif page == "review":
        form = ReviewForm()
    elif page == "course":
        form = CourseForm()
    else:
        form = None

    context["form"] = form

    return render(request, template, context)

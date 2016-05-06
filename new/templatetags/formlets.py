"""
All of these drop a lumx form where they are called. Please note that you must
have new.js loaded and lumx dependencies included.
"""
from django import template


register = template.Library()


@register.inclusion_tag("new/tags/professor.html")
def new_professor(is_edit=False):
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"is_edit": is_edit}


@register.inclusion_tag("new/tags/new_professor_popup.html")
def new_professor_popup(is_edit=False):
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"is_edit": is_edit}


@register.inclusion_tag("new/tags/course.html")
def new_course():
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {}


@register.inclusion_tag("new/tags/school.html")
def new_school(form, is_popup=False, is_edit=False):
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"form": form, "is_popup": is_popup, "is_edit": is_edit}


@register.inclusion_tag("new/tags/school_popup.html")
def new_school_popup(form, is_edit=False):
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"form": form, "is_edit": is_edit}


@register.inclusion_tag("new/tags/department.html")
def new_department():
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {}


@register.inclusion_tag("new/tags/review.html")
def new_review(is_edit=False):
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"is_edit": is_edit}


@register.inclusion_tag("new/tags/review_popup.html")
def new_review_popup(is_edit=False):
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"is_edit": is_edit}


@register.inclusion_tag("new/tags/field.html")
def new_field():
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {}


@register.inclusion_tag("new/tags/field_category.html")
def new_field_category():
    """
    Must be within a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {}


@register.inclusion_tag("new/tags/comment_popup.html")
def new_comment_popup(review):
    """
    Must be whithin a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"review": review}


@register.inclusion_tag("new/tags/comment.html")
def new_comment(review):
    """
    Must be whithin a ng-controller="form-handler" with a parameter for this
    form model.
    """
    return {"review": review}


@register.inclusion_tag("new/tags/report.html")
def new_report(instance):
    """
    Given an instance of a model, gives a form for reporting it.
    """
    return {"model": type(instance), "instance": instance}


@register.inclusion_tag("new/tags/resolve_report.html")
def resolve_report(id, instance):
    """
    Given a report id, gives a form to resolve it..
    """
    return {"model": type(instance), "instance": instance, "id": id}

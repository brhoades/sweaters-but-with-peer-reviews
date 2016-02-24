"""
All of these drop a lumx form where they are called. Please note that you must
have new.js loaded and lumx dependencies included.
"""
from django import template


register = template.Library()


@register.inclusion_tag("new/tags/professor.html")
def new_professor():
    return {}


@register.inclusion_tag("new/tags/course.html")
def new_course():
    return {}


@register.inclusion_tag("new/tags/school.html")
def new_school():
    return {}


@register.inclusion_tag("new/tags/department.html")
def new_department():
    return {}


@register.inclusion_tag("new/tags/review.html")
def new_review():
    return {}


@register.inclusion_tag("new/tags/field.html")
def new_field():
    return {}


@register.inclusion_tag("new/tags/field_category.html")
def new_field_category():
    return {}

from django import template
from django.shortcuts import render, redirect, get_object_or_404

register = template.Library()


@register.inclusion_tag("browse/tags/review_card.html")
def review_card(review_data, vote_data, can_vote=True):
    """
    Must have base.scss and reviews.scss included.
    Must have index.js included for voting to work.

    Returns a review card with the provided data.

    If can_vote is True, it renders vote buttons.
    """
    return {"review": review_data, "vote": vote_data,
            "can_vote": can_vote}


@register.inclusion_tag("browse/tags/mini_review.html")
def mini_review(review_id=0):
    """
    View a single review given an
    """

    return {}

from django import template

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


@register.inclusion_tag("browse/tags/professor_card.html")
def professor_card(professor):
    """
    Displays a professor card for the provided professor.
    """
    return {"professor": professor}


@register.inclusion_tag("browse/tags/school_card.html")
def school_card(school):
    """
    Displays a school card for the provided school.
    """
    return {"school": school}

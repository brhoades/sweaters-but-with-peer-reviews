"""
This file should have functions which facilitate browsing... getting votes,
for example.
"""
import math

from browse.models import Review, ReviewVote


def _get_all_review_votes(request, review_filter={}):
    """
    Simply returns a list of zipped reviews and votes.

    :rtype: list
    """

    reviewList = Review.objects.filter(**review_filter).order_by("-created_ts")

    voteList = []

    if request.user.is_authenticated():
        for review in reviewList:
            vote = ReviewVote.objects.filter(owner=request.user,
                                             target=review)

            # Add true if the vote is 'up', false if the vote is 'down'
            # Add None if the user has not voted on the review
            if vote.exists():
                voteList.append(vote[0].quality)
            else:
                voteList.append(None)
    else:
        voteList = [None for review in reviewList]

    return [(x, y,) for x, y in zip(reviewList, voteList)]


def paginate(page, model, key="-created_ts"):
    """
    Helps paging models.

    Returns a tuple:
        ([list of pages to show], current_page, [instances],
         startobject, endobject)

    Where the start object is an index of the object list.

    Can optionally pass it a key to sort by.
    """
    if page is None:
        page = 1
    else:
        page = int(page)

    # Someone make this less dumb
    num_per_page = 6
    # Our start and end indices of our model list.
    start = (page-1)*num_per_page
    end = start + num_per_page
    pages_to_show = 4  # the number of pages to show on the listing

    all_instances = model.objects.order_by(key)
    pages_available = math.ceil(len(all_instances) / num_per_page)

    if page > pages_available or page <= 0:
        start = 0
        end = 0
        page = 0

    # Our start index and end index for our page numbers.
    start_i = page - pages_to_show // 2
    end_i = page + pages_to_show // 2

    # If our page listing at the bottom of the page is above the number of
    # pages available/< 0, overflow it into the other side.
    if end_i > pages_available:
        start_i -= end_i - pages_available
        end_i = pages_available
        if start_i < 1:
            start_i = 1
    elif start_i < 1:
        end_i += 1 - start_i
        start_i = 1

        if end_i > pages_available:
            end_i = pages_available

    # If start is above the number of instances, make it equal to
    # the last num_per_page instances.
    if start > len(all_instances):
        start = len(all_instances) - num_per_page
        if start < 0:
            start = 0
        end = len(all_instances)

    return list(range(start_i, end_i+1)), page, all_instances, start, end

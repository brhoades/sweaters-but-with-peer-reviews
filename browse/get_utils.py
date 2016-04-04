"""
This file should have functions which facilitate browsing... getting votes,
for example.
"""

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

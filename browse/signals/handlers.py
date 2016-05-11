from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

import random

from browse.models import Log, Review, PeerReview
from new.utils import MODEL_MAP


@receiver(post_save)
def log_save(sender, instance, created, *args, **kwargs):
    """
    Creates a log entry for every creation / modification.
    """
    if instance.__class__.__name__.lower() not in MODEL_MAP:
        return

    if instance.__class__.__name__ == "Log":
        return

    owner = None
    if hasattr(instance, "created_by"):
        owner = instance.created_by
    elif hasattr(instance, "owner"):
        owner = instance.owner

    type = Log.ADD
    if not created:
        type = Log.MODIFY

    log = Log.create(instance, instance.id, type, owner=owner)
    log.save()


@receiver(post_delete)
def log_delete(sender, instance, *args, **kwargs):
    """
    Creates a log entry for every deletion.
    """
    if instance.__class__.__name__.lower() not in MODEL_MAP:
        return

    if instance.__class__.__name__ == "Log":
        return

    if hasattr(instance, "created_by"):
        owner = instance.created_by
    elif hasattr(instance, "owner"):
        owner = instance.owner
    else:
        owner = None

    log = Log.create(instance, instance.id, Log.DELETE, owner=owner)
    log.save()

@receiver(post_save, sender=Review)
def generatePeerReviews(sender, instance, created, **kwargs):
    """
    Generates PeerReviews when a Review object is created.
      Sender - the model (which is  defined in the decorator.)
      Instance - the instance of the model that triggered the call.
                  Here, this is simply the review.
      created - boolean value. (True if the object save that triggered the
                call was a newly created entry)
    """
    if created:
        numUsers = User.objects.count()
        for i in range(3):
            randUser = User.objects.get(id=(random.randint(1,numUsers)))
            newReview = PeerReview.objects.get_or_create(target=instance, 
                                                         owner=randUser)

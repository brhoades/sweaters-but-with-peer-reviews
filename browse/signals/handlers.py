from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from browse.models import Log
from new.utils import MODEL_MAP


@receiver(post_save)
def log_save(sender, instance, *args, **kwargs):
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
    if hasattr(instance, "updated") and instance.updated():
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

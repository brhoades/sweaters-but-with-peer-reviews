from django.test import TestCase
import random


def srs(model):
    """
    Get a Single Random Sample from a passed model. Just a simple alias.
    """
    return random.sample(list(model.objects.all()), 1)[0]

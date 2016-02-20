

def srs(model):
    """
    Get a Single Random Sample from a passed model. Just a simple alias.
    """
    return model.objects.order_by('?').first()

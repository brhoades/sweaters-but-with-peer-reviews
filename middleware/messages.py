from django.contrib import messages


def messages_processor(request):
    """
    This function provides whatever messages there are to be served to every
    single page.
    """
    return {"messages": messages.get_messages(request)}

from django.apps import AppConfig


"""
This file simply registers our signal handlers at the appropriate time on
application launch.
"""


class BrowseConfig(AppConfig):
    name = 'browse'
    verbose_name = "Peer Reviewed Professor Browse"

    def ready(self):
        """
        Initializes our signal handlers at runtime.
        """
        import browse.signals.handlers  # noqa (this makes flake8 ignore this)

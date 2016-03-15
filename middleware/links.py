from collections import OrderedDict


def link_processor(request):
    """
    This class provides, to all pages, a dict of links called "page_links".
    These links contain {"name": "tag"} for a name of a page to a view tag.

    These are used to automatically populate the sidebars.
    """
    # These are names which go to url tags.
    SIDEBAR_URLS = OrderedDict()
    SIDEBAR_URLS["Index"] = "index"
    SIDEBAR_URLS["Schools"] = "schools"
    SIDEBAR_URLS["Professors"] = "professors"
    SIDEBAR_URLS["Reviews"] = "reviews_overview"
    return {"page_links": SIDEBAR_URLS.items()}

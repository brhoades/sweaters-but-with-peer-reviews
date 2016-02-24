from django import template

register = template.Library()


@register.inclusion_tag("browse/tags/login.html")
def login(messages=[]):
    return {"messages": messages}


@register.inclusion_tag("browse/tags/login_popup.html")
def login_popup(messages=[]):
    return {"messages": messages}

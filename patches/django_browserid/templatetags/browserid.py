from django import template

from fancy_tag import fancy_tag


register = template.Library()


@fancy_tag(register, takes_context=True)
def browserid_info(context, **kwargs):
    # JJW 10/22/13 https://github.com/mozilla/django-browserid/issues/145
    if context.get('browserid_info'):
        return context['browserid_info'](**kwargs)


@fancy_tag(register, takes_context=True)
def browserid_login(context, **kwargs):
    return context['browserid_login'](**kwargs)


@fancy_tag(register, takes_context=True)
def browserid_logout(context, **kwargs):
    return context['browserid_logout'](**kwargs)


@fancy_tag(register, takes_context=True)
def browserid_js(context, **kwargs):
    return context['browserid_js'](**kwargs)

@fancy_tag(register, takes_context=True)
def browserid_css(context, **kwargs):
    return context['browserid_css'](**kwargs)

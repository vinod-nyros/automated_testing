"""
Context processors for the Home app, which include login / registration via Userena.

These return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

#from django.conf import settings as django_settings
#from django.db.models import get_models, Manager
#from django.utils.safestring import mark_safe

from userena.forms import SignupForm, AuthenticationForm


#### module globals

trace = 0


#### Context Processors

def registration_forms (request):
    return {
        'signup_form': SignupForm,
        'signin_form': AuthenticationForm,
    }


def cart_variables (request):
    from helpers import SessionHelper

    seshelp = SessionHelper (request.session)
    totqty, grandtot = seshelp.cart_totals()

    return {
        'cart_totqty': totqty,
        'cart_grandtot': grandtot,
    }


def environment (request):
    import os
    return os.environ

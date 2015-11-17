from django import forms
from django.forms import ModelForm
from models import *
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

from userena import settings as userena_settings
from userena.models import UserenaSignup
from userena.utils import get_profile_model, get_user_model

import random
from collections import OrderedDict

attrs_dict = {'class': 'required'}

USERNAME_RE = r'^[\.\w]+$'


## contact-us page

class ContactForm(forms.Form):
    topics = (
        ('Quote request', 'Quote request'),
        ('Network design services', 'Network design services'),
        ('System Architecture services', 'System Architecture services'),
        ('Hosting services', 'Hosting services'),
        ('Cloud provisioning and design services', 'Cloud provisioning and design services'),
        ('Open Source migration services', 'Open Source migration services'),
        ('Technical Support', 'Technical Support'),
        ('Special or quantity pricing', 'Special or quantity pricing'),
        ('Other', 'Other'),
    )
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=128)
    topic = forms.ChoiceField(choices=topics)
    description = forms.CharField (widget = forms.Textarea(attrs={'rows' : '2', 'cols':'60'}), required=False, label = 'Topic description (If "Other")')
    body = forms.CharField (widget = forms.Textarea(attrs={'rows' : '3', 'cols':'60'}), label = 'Main Body of message' )



## Email signup box

class SignupForm(forms.Form):
    """
    Form for creating a new user account.

    Validates that the requested username and e-mail is not already in use.
    Also requires the password to be entered twice.

    """
    username = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Create password"),required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repeat password"),required=False)


    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already in use.
        Also validates that the username is not listed in
        ``USERENA_FORBIDDEN_USERNAMES`` list.

        """
        try:
            user = get_user_model().objects.get(username__iexact=self.cleaned_data['username'])
        except get_user_model().DoesNotExist:
            pass
        else:
            if userena_settings.USERENA_ACTIVATION_REQUIRED and UserenaSignup.objects.filter(user__username__iexact=self.cleaned_data['username']).exclude(activation_key=userena_settings.USERENA_ACTIVATED):
                raise forms.ValidationError(_('This username is already taken but not confirmed. Please check your email for verification steps.'))
            raise forms.ValidationError(_('This username is already taken.'))
        if self.cleaned_data['username'].lower() in userena_settings.USERENA_FORBIDDEN_USERNAMES:
            raise forms.ValidationError(_('This username is not allowed.'))
        return self.cleaned_data['username']

    def clean_email(self):
        """ Validate that the e-mail address is unique. """
        if get_user_model().objects.filter(email__iexact=self.cleaned_data['email']):
            if userena_settings.USERENA_ACTIVATION_REQUIRED and UserenaSignup.objects.filter(user__email__iexact=self.cleaned_data['email']).exclude(activation_key=userena_settings.USERENA_ACTIVATED):
                raise forms.ValidationError(_('This email is already in use but not confirmed. Please check your email for verification steps.'))
            raise forms.ValidationError(_('This email is already in use. Please supply a different email.'))
        return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('The two password fields didn\'t match.'))
        return self.cleaned_data

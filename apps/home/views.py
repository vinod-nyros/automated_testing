# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.conf.urls import url, patterns, include
from django.contrib.admin.views.decorators import staff_member_required

from home.models import FeaturedImage

#Email signup box
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

#from obdjects.classes import Obdject

#from apps.utils import minitags as tags
from utils import minitags as tags
from forms import *  # contact-us page forms

from django.template import RequestContext
from django.core.mail import send_mail


## Create user & send email - called from two places

new_user_welcome_template = '''
Welcome to eRacks!

Dear %s,

Thank you for signing up at eracks.com

- Your user is: %s (You can use email address also to login)
%s
You can manage your profile anytime by logging in to eRacks at:

http://%s/accounts/login

Sincerely,

The eRacks Team
info@eracks.com
'''

def create_new_user(form,request):
    pw = User.objects.make_random_password(length=8)
    username = form.cleaned_data['email']
    password1 = pw
    password_entered = False
    # if form.cleaned_data['username']:
    #     username = form.cleaned_data['username']
    try:
        if form.cleaned_data['username']:
            username = form.cleaned_data['username']
    except KeyError:
        username = form.cleaned_data['email']

    try:
        if form.cleaned_data['password1']:
            password_entered = True
            password1 = form.cleaned_data['password1']
        else:
            password1 = pw
    except KeyError:
        password1 = pw

    email = form.cleaned_data['email']
    user = User.objects.create_user(username, email, password1)
    user.save()

    if password_entered:
        password_msg = ""
    else:
        password_msg = "\n- Your password is: %s \n"%(password1)

    # getting emails from settings -mani
    user.email_user ('Welcome to eRacks!', new_user_welcome_template % (username,username,password_msg,request.get_host()), settings.INFO_EMAIL)

    return user,password_entered


## Contact-us page

contact_email_template = '''
{s.HOST_NAME} user contact form:

Name: {f[name]}
User: {u}
eMail: {f[email]}

Topic: {f[topic]}
Description (if other): {f[description]}

Body of message: {f[body]}

'''

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            email = request.POST.get('email', '')
            users = User.objects.filter(email=email)

            if users:
                user = users [0]  # pick first one, although there shouldn't be more than 1
                result = 'Thank you for contacting us "%s"' % user.username
            else:
                user, password_entered = create_new_user(form,request)
                result = 'Thank you for contacting us and welcome to eRacks!  Your user is "%s", and your password has been sent to you.' % user.username

            subject = "%s user contact from %s about %s" % (settings.HOST_NAME, user, form.cleaned_data['topic'])
            message = contact_email_template.format (s = settings, f = form.cleaned_data, u = user)
            to = settings.CONTACT_EMAILS
            fm = user.email
            send_mail (subject, message, fm, to, fail_silently=False)

            return render (request, 'base.html', {'content': mark_safe (tags.h3(result))})

        return render (request, 'contact.html', {'form': form}, context_instance = RequestContext(request))

    form = ContactForm()

    return  render (request, 'contact.html',
        dict (
            form=form,
            meta_title='Contact with eRacks - Contact Us',
            meta_keywords='Rack Mount Server, Open Source Systems',
            meta_description='We are always interested in hearing from you, for all of your queries please stay in touch on info@eracks.com or you can call us on (408)455-0010',
        ),
        context_instance = RequestContext(request))


## Email signup box

def user_signup(request,template_name='userena/signup_form.html', success_url=None):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user,password_entered = create_new_user(form,request)

            if password_entered:
                result = 'Thank you for signing up and welcome to eRacks - your username is "%s"' % user.username
            else:
                result = 'Thank you for signing up and welcome to eRacks - your username is "%s", and your password has been sent to your email' % user.username

            return render (request, 'base.html', {'content': mark_safe(tags.h3(result))})
    else:
        form = SignupForm()

    return render (request, 'userena/signup_form.html', {'form': form })


#### generate_xml section - MANI: let's move this to a utils module, or a script, yes?

from xml.dom import minidom
import datetime
from time import strftime
from products.models import Product

def generate_xml():
    doc = minidom.Document()
    root = doc.createElement('urlset')
    doc.appendChild(root)
    all_products = Product.objects.all()
    for l in all_products:
        leaf = doc.createElement('loc')
        lastmod = doc.createElement('lastmod')
        changefreq = doc.createElement('changefreq')
        priority = doc.createElement('priority')
        branch = doc.createElement('url')
        text = doc.createTextNode('https://eracks.com%s' % l.url)
        dateandtime = doc.createTextNode(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"+00:00")
        changefreq_text = doc.createTextNode('daily')
        priority_text = doc.createTextNode('1.0000')
        lastmod.appendChild(dateandtime)
        leaf.appendChild(text)
        changefreq.appendChild(changefreq_text)
        priority.appendChild(priority_text)
        branch.appendChild(leaf.cloneNode(True))
        branch.appendChild(lastmod)
        branch.appendChild(changefreq)
        branch.appendChild(priority)
        root.appendChild(branch)
    xml_str = doc.toprettyxml(indent="  ")
    with open("apps/home/static/sitemap_generated.xml", "w") as f:
        f.write(xml_str)

#### End generate_xml


@staff_member_required
def testresults(request):
    path=settings.MEDIA_ROOT+"/test_results_screens"
    img_list =os.listdir(path)
    return render_to_response('test_results.html',{'images':img_list})


def index (request):
    return  render (request, 'home.html',
        dict (
            featured_images = FeaturedImage.objects.published,
            meta_title = 'Rackmount Server, Open Source Systems, Linux Rackmount',
            meta_keywords = 'Rackmount Server, Rack Mount Server, Open Source Systems, Linux Rackmount',
            meta_description = 'We are the leading Open Source Systems features its own line of rack mount server and offer a wide array of services including security and network architecture services.',
        ),
        context_instance = RequestContext(request))



## legacy Obdjects stuff - TODO: refactor - 9/16/15 JJW

gone='''
index = Obdject (
    urlregex = r'^$',
    #urlpattern = (r'^$', self),
    #template = 'home.html',
    template = 'home.html',
    #CustomerImagePubObjects = CustomerImage.objects.published,
    #TestimonialPubObjects = Testimonial.objects.published,
    featured_images = FeaturedImage.objects.published,
    meta_title = 'Rackmount Server, Open Source Systems, Linux Rackmount',
    meta_keywords = 'Rackmount Server, Rack Mount Server, Open Source Systems, Linux Rackmount',
    meta_description = 'We are the leading Open Source Systems features its own line of rack mount server and offer a wide array of services including security and network architecture services.',
)

urlpatterns = patterns('',
    index.urlpattern
)

'''

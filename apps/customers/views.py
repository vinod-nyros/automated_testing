
from django.http import HttpResponse
from django.shortcuts import render
#from django.template import Template, RequestContext  # Context,
#from django.template.defaultfilters import slugify
#from django.utils import simplejson as json
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test

from customers.models import Customer, CustomerImage, Testimonial, Address
#from customers import templets
from orders.models import ImportedOrder

#from obdjects.classes import Obdject
#from apps.utils import minitags as tags
from utils import minitags as tags


## Add user to our mailing list, and create a user for them -

#### TODO:
# templateize - DONE
# polish the results-handling - use Django messages, not H3 tags: https://docs.djangoproject.com/en/1.4/ref/contrib/messages/
# refactor and DRY out with create_user

welcome_template = '''
Thank you and welcome to eRacks!

You have been added to our mailing list:

- Your user is: %s (same as your email address)

- Your password is: %s

You can manage your profile anytime by logging in to eRacks at:

http://eracks.com/accounts/login

Best Regards,

The eRacks Team
info@eracks.com
'''

def save_email(request):
    def msg (s):
        return render (request, 'base.html', { 'content': mark_safe (tags.h3 (s)) })

    email = request.POST.get ('email', '')

    if not email:
        return msg ('You must enter an email address to be added to the mailing list!')

    users = User.objects.filter (email=email)

    if users:
        user = users [0]  # pick first one, although there shouldn't be more than 1
        return msg ('This email is already present - and has a user of "%s"' % user.username)
    else:
        groups = Group.objects.filter (name='From Join Box On Website')
        pw = User.objects.make_random_password(length=8)
        user = User.objects.create_user (email, email, pw)

        if groups:
            user.groups.add (groups [0])

        user.save()
        user.email_user ('Welcome to eRacks!', welcome_template % (email, pw), 'info@eracks.com')
        return msg ('Thank you and welcome to eRacks! You have been added to our mailing list, your user is "%s", and your password has been sent to you.' % user.username)


@user_passes_test(lambda u: u.is_superuser)
def emails (request):
    #users = User.objects.values()
    users = User.objects.filter (is_active=True, is_staff=False, email__contains="@").order_by('-date_joined')  #.values()

    templet = '"%(username)s", "%(email)s", "%(first_name)s", "%(last_name)s", %(is_active)s, %(is_staff)s, %(is_superuser)s, %(date_joined)s, %(last_login)s'
    header = templet.replace ('%(','').replace (')s','') + ', source'

    #return HttpResponse ('\n'.join ([header] + [templet % u.__dict__ + ', "%s"' % (u.groups.all() [0] if u.groups.all() else '') for u in users]),
    #    content_type="text/csv")


    #### users
    thelist = [header]
    thelist += [templet % u.__dict__ + ', "%s"' % (u.groups.all() [0] if u.groups.all() else '') for u in users]


    #### customers
    #thelist += ['- - - customers - - -']

    customers = Customer.objects.filter (published=True).order_by ("-created")

    for c in customers:
        if c.email and c.email != c.user.email and not User.objects.filter(email=c.email):
            #print c, c.user.first_name, c.user.last_name, c.email, '2:', c.email2, 'U:', c.user.email
            thelist += [templet % dict (
                username    = c.user.username,
                email       = c.email,
                first_name  = c.organization,
                last_name   = c.title,
                is_active   = c.user.is_active,
                is_staff    = c.user.is_staff,
                is_superuser = c.user.is_superuser,
                date_joined = c.created,
                last_login  = c.user.last_login,
                ) + ', "Customer"']
        if c.email2 and c.email2 != c.user.email and not User.objects.filter(email=c.email2):
            #print c, c.user.first_name, c.user.last_name, c.email, '2:', c.email2, 'U:', c.user.email
            thelist += [templet % dict (
                username    = c.user.username,
                email       = c.email2,
                first_name  = c.organization,
                last_name   = c.title,
                is_active   = c.user.is_active,
                is_staff    = c.user.is_staff,
                is_superuser = c.user.is_superuser,
                date_joined = c.created,
                last_login  = c.user.last_login,
                ) + ', "Customer"']


    #### Address emails
    #thelist += ['- - - address emmails - - -']
    addresses = Address.objects.filter (published=True).order_by ("-created")

    for a in addresses:
        if a.email and not User.objects.filter(email=a.email):
            thelist += [templet % dict (
                username    = a.customer.user.username,
                email       = a.email,
                first_name  = a.nickname,
                last_name   = a.name,
                is_active   = a.customer.user.is_active,
                is_staff    = a.customer.user.is_staff,
                is_superuser = a.customer.user.is_superuser,
                date_joined = a.created,
                last_login  = a.customer.user.last_login,
                ) + ', "Address"']


    #### legacy zope order emails
    #thelist += ['- - - legacy Zope emails - - -']
    #statuses = []
    #orders = ImportedOrder.objects.filter (orderstatus__in=statuses).order_by ("orderstatus", "-orderdate")
    #orders = ImportedOrder.objects.all().order_by ("orderstatus", "-orderdate")
    orders = ImportedOrder.objects.exclude (orderstatus__in=['fraud']).order_by ("orderstatus", "-orderdate")

    for o in orders:
        if o.email and not User.objects.filter(email=o.email):
            thelist += [templet % dict (
                username    = o.ordernum,
                email       = o.email,
                first_name  = o.name(),
                last_name   = o.org(),
                is_active   = False,
                is_staff    = False,
                is_superuser = False,
                date_joined = o.orderdate,
                last_login  = o.shipdate,
                ) + ', "Legacy Zope Order: %s"' % o.orderstatus]

    return HttpResponse ('\n'.join (thelist), content_type="text/csv")


#from utils import Breadcrumb
#customers_breadcrumb = Breadcrumb ('Customers', 'Customers and Testimonials', '/customers/')

# no longer using generic views in urls.py
def index (request):
    customers = CustomerImage.objects.filter (published=True)
    testimonials = Testimonial.objects.filter (published=True)
    cachetime=36000

    return render (request, 'customers.html', dict (
        breadcrumbs=True, # (customers_breadcrumb,),      # True,
        title='Customers and Testimonials',
        customers=customers,
        testimonials=testimonials,
        cachetime=cachetime,
        request=request,  # Why do I need to add this?!  'render' doesn't seem to work
    ))


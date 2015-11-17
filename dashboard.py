"""

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'eracks11.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for eRacks admin
    """
    #Administration part
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.Group(
            _('Administration'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('Authentication and Authorization'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.auth.*',),
                ),
                modules.ModelList(
                    _('Redirects'),
                    column=1,
                    collapsible=False,
                    # css_classes=('collapse closed',),
                    models=('django.contrib.redirects.models.*',),
                ),
                modules.ModelList(
                    _('Sites'),
                    column=1,
                    collapsible=False,
                    # css_classes=('collapse closed',),
                    models=('django.contrib.sites.models.*',),
                )
            ]
        ))

        #Home Page part
        self.children.append(modules.Group(
            _('Home Page'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('Home'),
                    column=1,
                    collapsible=False,
                    models=('home.models.*',),
                ),
                modules.ModelList(
                    _('Bloglets'),
                    column=1,
                    collapsible=False,
                    # css_classes=('collapse closed',),
                    models=('bloglets.models.*',),
                ),
                modules.ModelList(
                    _('quickpages'),
                    column=1,
                    collapsible=False,
                    # css_classes=('collapse closed',),
                    models=('quickpages.*',),
                )
            ]
        ))

        #Orders and Customers part
        self.children.append(modules.Group(
            _('Orders and Customers'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('Customers'),
                    column=1,
                    collapsible=False,
                    models=('customers.models.*',),
                ),
                modules.ModelList(
                    _('Orders'),
                    column=1,
                    collapsible=False,
                    # css_classes=('collapse closed',),
                    models=('orders.models.*',),
                ),
            ]
        ))

        #Categories and products
        self.children.append(modules.Group(
            _('Categories and products'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('Products'),
                    column=1,
                    collapsible=False,
                    models=('products.models.*',),
                ),
            ]
        ))

        #Other Applications part
        self.children.append(modules.Group(
            _('Other Application'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('CA tax'),
                    column=1,
                    collapsible=False,
                    models=('catax.models.*',),
                ),
                modules.ModelList(
                    _('Quotes'),
                    column=1,
                    collapsible=False,
                    models=('quotes.models.*',),
                ),
                modules.ModelList(
                    _('SQL Web Shell'),
                    column=1,
                    collapsible=False,
                    models=('sqls.models.*',),
                ),
                modules.ModelList(
                    _('Python Web Shell'),
                    column=1,
                    collapsible=False,
                    models=('webshell.models.*',),
                ),
                modules.ModelList(
                    _('Email Extras (GPG)'),
                    column=1,
                    collapsible=False,
                    models=('email_extras.models.*',),
                ),
                #modules.ModelList(
                #    _('social_auth'),
                #    column=1,
                #    collapsible=False,
                #    models=('social_auth.*',),
                #),
                modules.ModelList(
                    _('Social Auth'),
                    column=1,
                    collapsible=False,
                    models=('social.apps.django_app.default.*',),
                ),
                modules.ModelList(
                    _('Taggit'),
                    column=1,
                    collapsible=False,
                    models=('taggit.models.*',),
                ),

                #Obdjects models moved to Quickpages and its showing as quick snippets
                # modules.ModelList(
                #     _('Obdjects'),
                #     column=1,
                #     collapsible=False,
                #     models=('obdjects.models.*',),
                # ),
            ]
        ))

        # Media / File Management - Grappelli's Filebrowser.
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # Django IDE
        self.children.append(modules.LinkList(
            _('Django IDE'),
            column=2,
            children=[
                {
                    'title': _('DjangoIDE'),
                    'url': '/djide/',
                    'external': False,
                },
            ]
        ))

        # append a link list module for Imports / CSV Imports
        self.children.append(modules.LinkList(
            _('Imports'),
            column=2,
            children=[
                {
                    'title': _('CSVImport'),
                    'url': '/admin/csvimport/',
                    'external': False,
                },
            ]
        ))

        # Utils
        self.children.append(modules.LinkList(
            _('Utils'),
            column=2,
            children=[
                {
                    'title': _('URLs'),
                    'url': '/utils/urls/',
                    'external': False,
                },
                {
                    'title': _('Clear Cache'),
                    'url': '/utils/clearcache/',
                    'external': False,
                },
                {
                    'title': _('Collect static files'),
                    'url': '/utils/collect_static/',
                    'external': False,
                },
            ]
        ))

        # Orders module utils
        self.children.append(modules.LinkList(
            _('Orders Utils'),
            column=2,
            children=[
                {
                    'title': _('Your current session'),
                    'url': '/session/',
                    'external': False,
                },
                {
                    'title': _('Legacy order admin grid'),
                    'url': '/admin_order_grid/',
                    'external': False,
                },
            ]
        ))



        # append another link list module for "support".
        # self.children.append(modules.LinkList(
        #     _('Support'),
        #     column=2,
        #     children=[
        #         {
        #             'title': _('Django Documentation'),
        #             'url': 'http://docs.djangoproject.com/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Grappelli Documentation'),
        #             'url': 'http://packages.python.org/django-grappelli/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Grappelli Google-Code'),
        #             'url': 'http://code.google.com/p/django-grappelli/',
        #             'external': True,
        #         },
        #     ]
        # ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=15
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=20,
            collapsible=False,
            column=3,
        ))



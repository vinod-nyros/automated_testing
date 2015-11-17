import os.path
from django.utils.translation import ugettext_lazy as _

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

THEMES = ({
    'name': _("Minimalist Theme"),
    'description': _("Minimalist Theme #1"),
    'screenshot': "/static/minimalist/Screenshot-Minimalist.png",
    'template_dir': "minimalist",
    # If you will use TEMPLATE_LOADERS method described in setup section,
    # than you should specify full path
    #'template_dir': os.path.join(PROJECT_ROOT, "templates/theme1"),
    'static_url': "/static/minimalist/",
},
{
    'name': _("TShop Theme"),
    'description': _("TShop Theme #2"),
    'screenshot': "/static/tshop/Screenshot-TSHOP.png",
    'template_dir': "tshop",
    # If you will use TEMPLATE_LOADERS method described in setup section,
    # than you should specify full path
    #'template_dir': os.path.join(PROJECT_ROOT, "templates/theme2"),
    'static_url': "/static/tshop/",
})

DEFAULT_THEME = 1

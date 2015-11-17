import sys
import pprint

from updater import sesurl

from django_eracks.apps.utils.minitags2 import TagStream  #FormattedTagStream


def reload_django_settings():
    import os
    os.environ ['DJANGO_SETTINGS_MODULE'] = 'django_eracks.settings'
    import django_eracks
    import django_eracks.settings as settings
    reload (django_eracks)
    reload (django_eracks.apps)
    reload (django_eracks.apps.utils)
    reload (django_eracks.apps.utils.minitags2)
    reload (settings)

    from django.conf import settings
    settings._wrapped = None  # force a reload
    settings._setup()  # but do it manually anyway
    #return django_eracks.apps.utils.minitags2.FormattedTagStream
    return pprint.pformat (settings._wrapped.__dict__)


def test():
    from django_eracks.apps.legacy.models import Product
    from django_eracks.apps.utils.minitags2 import TagItem, TagItemList
    #prods = Product.objects.filter (current__in=['t','T'])
    prods = Product.objects.filter (published=True)
    content = str(TagItemList(prods).li)
    result = str (TagItem (content).html.body.ul)
    return result
    return str (prods.count())


def getsession (self):
  return getattr (self, 'session', self.aq_parent.session)

def cartcontents (self):
  ses = getsession (self)

  grandtot = 0
  totqty = 0

  if ses.has_key ('cart'):
    cart = ses ['cart']
    
    for line in cart.values():
      qty = line ['qty']
      totqty = totqty + qty
      grandtot = grandtot + qty * line ['totprice']

  return (totqty, grandtot)


def django_cart_box (self):
    carturl = sesurl (self.session, self.REQUEST, 'cart', 1)
    checkouturl = sesurl (self.session, self.REQUEST, 'cart', 2)

    (totqty, grandtot) = cartcontents (self)

    if not totqty: return ''

    return TagStream() \
            .div (cls="box xsmall center") \
            .div('Your eRacks cart', cls="boxtitle small") \
            .img (src='/images/cart', alt='Shopping Cart Image') \
            .a(' %i item%s $%8.2f total' % (totqty, 's'*int(totqty!=1), grandtot), href=carturl).br \
            .a ('View Cart', href=carturl) \
            .span (' &middot; ') \
            .a ('Checkout', href=checkouturl) \
            .render()


  
# - - - old - - -

def reload_django_settings_test_project():
    import os
    os.environ ['DJANGO_SETTINGS_MODULE'] = 'test_django_project.settings'
    #import django.conf
    #reload (django.conf.global_settings)
    import test_django_project
    import test_django_project.settings as settings
    #try:
    #    del sys.path ['test_django_project.settings']
    #from test_django_project import settings
    reload (test_django_project)
    reload (settings)

    from django.conf import settings
    settings._wrapped = None  # force a reload
    settings._setup()  # but do it manually anyway
    #reload (settings)
    #return pprint.pformat (sys.path)  # + [__file__,  __module__])
    #return 'Aha:' + pprint.pformat (sys.modules)
    #return 'proj refcount:' + str(sys.getrefcount (test_django_project)) + ' settings refcount:' + str (sys.getrefcount (settings))
    return pprint.pformat (settings._wrapped.__dict__) # .DATABASES)
    return pprint.pformat (settings.DATABASES)


def syspath2():
    import os
    os.environ ['DJANGO_SETTINGS_MODULE'] = 'test_django_project.settings'
    from django.conf import settings
    settings._wrapped = None  # force a reload, but doesn't
    #settings._setup()  # so try doing it manually
    #del settings._wrapped.DATABASES
    return pprint.pformat (settings.DATABASES)
    return pprint.pformat (settings._wrapped.__dict__) # .DATABASES)


old='''
def boxtop (clr, txt):
  result = '<table width="100%" cellspacing="0" cellpadding="0" border="0">\n'       \
           ' <tr>\n'                                                                 \
           '  <td bgcolor="' + clr + '" align="center" valign="top" colspan="4">\n'  \
           '   <font face="Geneva, Helvetica" size="2" color="#000000">\n' +          \
                txt +                                                                \
           '   </font>\n'                                                            \
           '  </td>\n'                                                               \
           ' </tr>'
  return result

def boxbottom (clr, pix):
  result = ' <tr height="2">\n'                                                        \
           '  <td colspan="4" bgcolor="' + clr + '">' + pix2 + '</td>\n'                \
           ' </tr>\n'                                                                  \
           ' <tr height="5"><td colspan="4" bgcolor="#ffffff">' + pix + '</td></tr>\n' \
           '</table>'
  return result
  
def boxside (clr):
  return '<td width="2" bgcolor="%s">%s</td>' % (clr, pix2)
  #return '<td bgcolor="%s">%s</td>' % (clr, pix2)
  
  
cartbox tail:  
    s = boxtop (clr, 'Your eRacks cart') + \
        '<tr nowrap>' + boxside (clr) + \
        ' <td valign="middle" align="center">' + \
        font (1, link (surl ('cart', 1), img (self, 'cart') + \
                               ' %i item%s' % (totqty, iff (totqty==1, '', 's')) + \
                               ' $%8.2f total' % grandtot) ) + '</td><td> </td>\n' + \
        boxside (clr) + '</tr>' + \
        '<tr nowrap>' + boxside (clr)  + \
        ' <td valign="middle" align="center">' + \
        font (1, link (surl ('cart', 1), 'View Cart') + '&nbsp&middot&nbsp' + \
                 link (surl ('checkout', 2), 'Checkout') ) + '</td><td> </td>\n' + \
        boxside (clr) + '</tr>' + \
        boxbottom (clr, pix)
  else:
    s = ''
    
  return s

'''
# -*- coding: utf-8 -*-

import os

try:
    import json
except ImportError:
    import simplejson as json

#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext  # Template, Context,
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

from utils import minitags as tags
from utils import Breadcrumb

from home.helpers import SessionHelper

from products.models import Product, Categories

from django.conf import settings

from django.contrib.sitemaps import Sitemap

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated

#### globals and functions

product_breadcrumb = Breadcrumb ('Products', 'eRacks Products', '/products/')

#@cache_function
def product_photos (product):
    return product.images.published()  #### HERE - either return just the fname tail, or change the template!

    # see also scripts/photos/import_photos for a smarter algorithm, and brahms too :)
    # but now, we just use the DB

    folder = os.path.join (settings.STATIC_ROOT, 'images','products', product.slug)
    try:
        #return os.listdir (folder)
        return  [f for f in os.listdir (folder)
                  if os.path.isfile (os.path.join (folder, f))
                  and os.stat (os.path.join (folder, f)).st_size > 22000  # TODO: check here for in images and unpublished
                ]
    except Exception, e:
        print e
        return []

#### View functions

def config (request, legacy_category=None):  # redirect legacy Zope URLs to new product page
    sku = request.GET.get ('sku')

    if legacy_category:
        category = slugify (legacy_category)
    else:
        product = Product.objects.filter (sku=sku)
        if product:
            category = product [0].category.slug
        else:
            raise Http404

    return HttpResponseRedirect ('/products/%s/%s' % (category, sku))


#def products (request):  # really categories
#    categories = Categories.objects.published()
#
#    return render_to_response('products.html', dict (
#            title="eRacks Product Categories",
#            categories=categories,
#            breadcrumbs=(product_breadcrumb,),
#        ), context_instance=RequestContext(request))


def categories (request):
    categories = Categories.objects.published()

    return render_to_response('categories.html', dict (
            title="eRacks Product Categories",
            categories=categories,
            breadcrumbs=(product_breadcrumb,),
        ), context_instance=RequestContext(request))


def category (request, category):
    categories = Categories.objects.published().filter (slug=category)

    if not categories:
        categories = Categories.objects.published().filter (name__iexact=category)
        if categories:
            return HttpResponseRedirect ('/products/%s/' % categories [0].slug)

    if not categories:
        raise Http404, "Unknown Category"  # allows for redirect lookup too

    category = categories [0]

    breadcrumbs = (
        product_breadcrumb,
        category
    )

    return render_to_response('category.html', dict (
            title=category.title or category.name,
            category=category,
            breadcrumbs=breadcrumbs,
            meta_title=category.meta_title,
            meta_keywords=category.meta_keywords,
            meta_description=category.meta_description,
        ), context_instance=RequestContext(request))


def product (request, category, sku):
    products = Product.objects.filter (sku__iexact=sku)

    if products:
        product = products [0]
        if product.sku != sku:
            return HttpResponseRedirect (product.url)
        if product.category.slug != category:
            return HttpResponseRedirect (product.url)
    else:
        raise Http404, "Unknown Product"

    edit = request.GET.get ('edit', None)

    ses_helper = SessionHelper (request.session)

    if not edit:
        ses_helper.fill (product)
    else:
        assert request.session.get ('prod', None)

    breadcrumbs = (
        product_breadcrumb,
        product.category,
        product,
    )

    photos_list = [str(t) for t in product_photos (product)]
    photos = mark_safe ('\n'.join (photos_list))

    return render_to_response ('product.html', dict (
            title=product.title or product.name,
            product=product,
            breadcrumbs=breadcrumbs,
            meta_title=product.meta_title,
            meta_keywords=product.meta_keywords,
            meta_description=product.meta_description,
            photos=photos,
            photos_list=photos_list,
            js_bottom=mark_safe (tags.script (config_grid_js, type='text/javascript')),
        ), context_instance=RequestContext(request))



#### Ajax views and supporting

#@is_ajax or ajax_required...
def update_grid (request):
    ses_helper = SessionHelper (request.session)
    results = ses_helper.update (request)
    return HttpResponse (json.dumps (results), content_type='application/json')


#### configgrid view with js

config_grid_js='''
function update_config (e) {
    console.log ($('.configform').serialize());
    if (e) {
        console.log ('ITEM CHANGED:');
        console.log (e.currentTarget);
        console.log ($(e.target).find ('option:selected'));
    }

    $.post ("/products/update_grid/", $('.configform').serialize(), function(json) {
        console.log (json);
        $('#config_summary .price b').html ('$' + json.price);
        $('#config_summary .summary').html ('<b>Configuration Summary:</b><br>' + json.summary);

        $.each(json.optchoices, function(key, val) {  // it's an array, so keys are 0
            console.log (key, val);
            console.log ('#' + val.optid + ' .info');
            if (val.choicename)
                $('#' + val.optid + ' .info').html (val.choicename);
            if (val.choiceblurb)
                $('#' + val.optid + ' .info').attr ('title', val.choiceblurb);
            //if (val.optprice)
            $('#' + val.optid + ' .optprice').html ('$' + val.optprice);
        });
    }).error (function(err) {
        console.log ('post error:' + err);
        window.location.reload();   // likely the back button, prod is no longer there, so reload
    });
}

$(document).ready(function() { // JJW changed this to load 1/10/13, was firing before GET completed, causing inv inx
//$(document).load(function() {  // nope, doesn't fire at all now :(
    //update_config();

    $('.configgrid select[name="choiceid"]').change (update_config);
    $('.configgrid select[name="choiceqty"]').change (update_config);
});
'''


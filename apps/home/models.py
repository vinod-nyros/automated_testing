from django.db import models
from django.utils.safestring import mark_safe

from apps.utils.managers import PublishedManager
from apps.utils import minitags as tags

from products.models import Product

from filebrowser.fields import FileBrowseField


#### Globals

trace = 0


#### Model classes

class FeaturedImage (models.Model):
    #image       = models.ImageField  (upload_to = 'images/customers/')
    #image2      = FilerImageField    (null=True, blank=True)
    image       = FileBrowseField     (max_length=200, directory="images/", extensions=[".jpg",".jpeg",".png",".gif"]) #, blank=True, null=True)
    link        = models.CharField    (max_length=100,     help_text="Product or page to link to - relative links OK")
    title       = models.CharField    (max_length = 100, blank=True, help_text="Mouseover title - optional")
    caption     = models.CharField    (max_length = 100, blank=True, help_text="Image / Slide caption - optional, shown across bottom of image, such as &lt;h2>My Caption&lt;/h2>")
    #html_overlay = models.TextField  (blank=True,         help_text="HTML / Text overlay over image - optional")
    product     = models.ForeignKey   (Product, null=True, blank=True, help_text='Product the featured image is talking about, optional, can use caption instead')
    sortorder   = models.IntegerField (default=100,        help_text="Default order the slideshow is shown in")

    created     = models.DateTimeField (auto_now_add=True)
    updated     = models.DateTimeField (auto_now=True)
    published   = models.BooleanField (default=True)

    objects     = PublishedManager()

    def __unicode__ (self):
        return self.caption or self.title or self.image.url

    class Meta:
        ordering = ["sortorder"]

    def as_img (self):
        if trace: print self
        kw = dict (src=self.image.url,
                #d='#featured_%s' % self.id,
                alt=self.caption,
                title=self.title,
                data_link=self.link,
            )
        kw['data-link']=kw.pop('data_link')

        return mark_safe (tags.img (**kw))

        # return mark_safe ('<img src="%s" alt="%s" title="%s" data-link="%s"/>' % (self.image.url, self.caption, self.title, self.link))
        # tagstream / TagGen?


    def as_caption (self):
        rslt = tags.span (self.caption, cls='orbit-caption', d='featured_caption_%s' % self.id) if self.caption else ''

        return mark_safe (rslt)


    def as_content (self):
        kw = dict (
            cls='content',
            d='#featured_%s' % self.id
        )

        if self.caption:
            kw ['data-caption'] = '#featured_caption_%s' % self.id

        rslt = tags.div (tags.a (self.as_img(), href=self.link), **kw)

        return mark_safe (rslt)

    # NYI
    #def as_html_overlay_caption (self):
    #    if trace: print self
    #    return mark_safe (tags.img (src=self.image.url, alt=self.caption, title=self.title))


#### Set up single-seq tables (org fm legacy eracks db)

from apps import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=FeaturedImage)

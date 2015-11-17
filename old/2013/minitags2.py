# minitags2 library Copyright (c) 2011 Joseph J Wolff all rights reserved

from copy import deepcopy


#### globals

trace = 0
trailing_slash = '' # or set to ' /' for xhtml-compliance

# html 4.01 / xhtml 1.0 single tag list - from http://www.w3schools.com/tags/default.asp

single_tags = ['area','base','basefont','br','col','frame','hr','img','input','link','meta','param',]


### Classes

class Tag:
    def __init__ (self, tag=None, trailing_slash=trailing_slash, **kw):
        self.tag = tag.lower()
        self.single_tag = self.tag in single_tags
        # self.single_tag_after - for hr, etc
        self.trailing_slash = trailing_slash
        self.kw = kw
        if trace: print self

    def attrmap (self, k):
        return dict (cls='class', fr='for', d='id').get (k, k)

    def dict2attrs (self, kw):
        if kw:
            return ' ' + ' '.join (('='.join ((self.attrmap (k),'"%s"' % str(v))) for k,v in kw.items()))
        else:
            return ''

    def __call__ (self, content, **kw):
        if trace: print content, args, kw

        if self.single_tag:
            result = '<%s%s%s>%s' % (self.tag, self.dict2attrs (kw), self.trailing_slash, content)
        else:
            result = '<%s%s>%s</%s>' % (self.tag, self.dict2attrs (kw), content, self.tag)

        return result


class TagItem (object):   # itm = any object - checked for attrs
    def __init__ (self, itm, content_attr=None, stack=[], **kw):
        self.itm = itm
        self.stack = stack
        self.content_attr = content_attr
        self.kw = self._update_keywords (kw)

    def _push (self, x):
        return self.stack.append (x)

    def _pop(self):
        return self.stack.pop()

    def _update_keywords (self, kw):
        chase_attrs = dict ([(k, getattr (self.itm, v)) for k,v in kw.items() if hasattr (self.itm, v)])
        for k,v in kw.items():
            if hasattr (self.itm, v):
                new_v = getattr (self.itm, v)
                if callable (new_v):
                    try: 
                        new_v = new_v()
                        kw [k] = new_v
                    except: 
                        pass
                else:
                    kw [k] = new_v
        return kw

    def __getattr__ (self, name):
        self._push (Tag (name))
        return self  # chainable

    def __call__ (self, **kw):
        self._push (kw)
        return self  # chainable

    def __str__ (self):
        kw = self.kw

        if self.content_attr:
            s = str(getattr (self.itm, self.content_attr, self.content_attr))
        else:
            s = str (self.itm)

        while len (self.stack):
            x = self._pop()
            if callable (x):
                s = x (s, **kw)
                kw = self.kw
            else:
                kw = self._update_keywords (x)

        return s


class TagItemList (TagItem):
    def __init__ (self, lst, content_attr=None, **kw):
        self.lst = lst
        self.stack = []
        self.content_attr = content_attr
        self.kw = kw

    def __str__ (self):
        s = ''

        for itm in self.lst:
            ti = TagItem (itm, self.content_attr, deepcopy(self.stack), **self.kw)
            s += str(ti) + '\n'

        return s


#### Main for standalone testing

if __name__ == '__main__':
    from product.models import Category

    lst = Category.objects.filter (name__icontains='acc')
    #print TagItemList (lst, content_attr='name').li(cls='cat', d='slug').br.img(src='main_image', title='description').div.span.a(href='get_absolute_url')

    #for c in lst:
    #    print c.slug, c

# TODO: implem attr_nofollow, check for dict entries too, not just attrs, also improve 'callable' semantics in stack handling

# TODO 6/29/11 implem closure upon passing in *args - treat it like a single tag - allows for full form handling, even complete (simple) web pages

# TODO 6/29/11: impleme TagItemTemplate - pass in the strings you want to be put as pytemplate strings in the template - then call render to render
# could even do TagDjangoTemplate, TagPythonTemplate, TagPythonDictTempalte, etc

    #class TagItemTemplate (TagItem):
    #    def ...

    # like this:

    ti = str(TagItem ('{0.name}').li(cls='cat', d='{0.slug}').br.img(src='{0.main_image}', title='{0.description}').div.span.a(href='{0.get_absolute_url}'))
    print ti

    for i in lst:
        print ti.format (i)

    # so would likely want to override call, str, and 'add 'render', 'prepare', and/or 'format'.
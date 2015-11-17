# minitags2 library Copyright (c) 2011 Joseph J Wolff all rights reserved


#### globals

trace = 0

# Set this to ' /' for xhtml-compliance
trailing_slash = ''

# html 4.01 / xhtml 1.0 single tag list - from http://www.w3schools.com/tags/default.asp
single_tags = ['area','base','basefont','br','col','frame','hr','img','input','link','meta','param',]

# Iterable test - strings are NOT iterable using this, which is exactly what we want
is_iterable = lambda x: hasattr (x, '__iter__')

# Shorten/avoid reserved words in keyword arguments
attrmap = lambda k: dict (cls='class', class_='class', fr='for', d='id', id_='id').get (k, k)


### Classes

class Tag:
    def __init__ (self, tag=None, trailing_slash=trailing_slash, **kw):
        self.tag = tag.lower()
        self.single_tag = self.tag in single_tags
        # self.single_tag_after - for hr, etc
        self.trailing_slash = trailing_slash
        self.kw = kw
        if trace: print 'INIT:', self, tag, kw

    def dict2attrs (self, kw):
        if kw:
            return ' ' + ' '.join (('='.join ((attrmap (k),'"%s"' % str(v))) for k,v in kw.items()))
        else:
            return ''

    def __call__ (self, content, *args, **kw):
        if trace: print 'CALL:', str(content) [:40], '...', args, kw

        if self.single_tag:
            result = '<%s%s%s>%s' % (self.tag, self.dict2attrs (kw), self.trailing_slash, content)
        elif args:
            result = '<%s%s>%s</%s>%s' % (self.tag, self.dict2attrs (kw), args[0], self.tag, content)
        else:
            result = '<%s%s>%s</%s>' % (self.tag, self.dict2attrs (kw), content, self.tag)

        return result


class TagStream (object):
    def __init__ (self):
        self.stack = []

    def _push (self, x):
        return self.stack.insert (0, x)  # build it upside down for iteration / reusability

    def __getattr__ (self, name):
        self._push (Tag (name))
        return self  # chainable

    def __call__ (self, *args, **kw):
        args = list (args)
        self._push ((args, kw))
        return self  # chainable

    # guaranteed a single item, not a list or *args
    def _render_item (self, itm):
        kw = {}
        args = []

        for x in self.stack:
            if callable (x):
                itm = x (itm, *args, **kw)
                kw = {}
                args = []
            else:
                args, kw = x

        return itm


    def render (self, *args):
        if len (args) > 1:
            return [self.render (contents) for contents in args]

        if args:
            contents = args [0]
        else:
            contents = ''

        if is_iterable (contents):
            return [self.render (content) for content in contents]

        return self._render_item (contents)



class Wrap (TagStream):
    def __init__ (self, itm, **kw):
        TagStream.__init__ (self)
        self.itm = itm

    def __str__ (self):
        return self.render (self.itm)


class ObjectTagStream (TagStream):
    def _render_item (self, itm):
        for parms in self.stack:
            if isinstance (parms, tuple) and len (parms) == 2:
                args, kw = parms

                for i, arg in enumerate (args):
                    if hasattr (itm, arg):
                        args [i] = getattr (itm, arg)

                for k,v in kw.items():
                    print k,v
                    if hasattr (itm, v):
                        kw [k] = getattr (itm, v)

        return TagStream._render_item (self, itm)


class ObjectTagStreamBoth (TagStream):
    def _render_item (self, itm):
        if isinstance (itm, dict):
            dct = itm
            print 'dct is itm:', dct
        else:
            if hasattr (itm, '__dict__'):
                dct = itm.__dict__
                print 'dct is itm.__dict__:', dct
            elif hasattr (itm, '__class__'):
                dct = itm.__class__.__dict__
                print 'dct is itm.__class__.__dict__:', dct
            else:
                dct = {}
                print 'dct is empty'

        for parms in self.stack:
            if isinstance (parms, tuple) and len (parms) == 2:
                args, kw = parms

                for i, arg in enumerate (args):
                    print i,arg
                    args [i] = getattr (itm, arg, arg % dct)

                for k,v in kw.items():
                    print k,v
                    kw [k] = getattr (itm, v, v % dct)

        return TagStream._render_item (self, itm)


#class ObjectTagStream2 (TagStream):  # Pre-Py 2.4 dict-replacement syntax compatible
class FormattedTagStream (TagStream):  # Pre-Py 2.4 dict-replacement syntax compatible
    def _render_item (self, itm):
        if not isinstance (itm, dict):
            if hasattr (itm, '__dict__'):
                itm = itm.__dict__
            else:
                raise Exception ('FormattedTagStream Item must be mapping type ot haver valid dictionary member')

        for parms in self.stack:
            if isinstance (parms, tuple) and len (parms) == 2:
                args, kw = parms

                for i, arg in enumerate (args):
                    args [i] = arg % itm

                for k,v in kw.items():
                    kw [k] = v % itm

        return TagStream._render_item (self, itm)

# http://docs.python.org/release/2.6.6/library/string.html#template-strings
# per PEP 292: http://www.python.org/dev/peps/pep-0292
class ObjectTagStream3 (TagStream):  # Py 2.4 & later template-string compatible
    def _render_item (self, itm):
        from string import Template

        if not isinstance (itm, dict):
            if hasattr (itm, '__dict__'):
                itm = itm.__dict__
            else:
                raise Exception ('ObjectTagStream3 Item must be mapping type')

        for parms in self.stack:
            if isinstance (parms, tuple) and len (parms) == 2:
                args, kw = parms

                for i, arg in enumerate (args):
                    args [i] = Template (arg).safe_substitute (itm)

                for k,v in kw.items():
                    kw [k] = Template (v).safe_substitute (itm)

        return TagStream._render_item (self, itm)


# http://docs.python.org/release/2.6.6/library/string.html#string-formatting
# per PEP 3101: http://www.python.org/dev/peps/pep-3101/
class ObjectTagStream4 (TagStream):  # Py 2.6 & later string-format compatible
    def _render_item (self, itm):
        if not isinstance (itm, dict):
            if hasattr (itm, '__dict__'):
                itm = itm.__dict__
            else:
                raise Exception ('ObjectTagStream4 Item must be mapping type')

        for parms in self.stack:
            if isinstance (parms, tuple) and len (parms) == 2:
                args, kw = parms

                for i, arg in enumerate (args):
                    print i, arg
                    args [i] = arg.format (**itm)

                for k,v in kw.items():
                    print k,v
                    kw [k] = v.format (**itm)

        return TagStream._render_item (self, itm)



# TODO:
#
# 7/16/11 So the real issues are: (1) when to close/roll up, and (2) when to fan out lists.
# May need intelligent tag proximity handling, eg table/tr/td, etc
# text and close and/or nest methods too
#
# Also: 'boolean_attrs' - selected, checked - if false, they don't appear; if true, just set to 1
#
# early July 2011:
# d lists / *args passed to
# d obj lookup
# d 2.4 py syntax?
# d py template (2.6 & later)
# Django templates
# integrate passed-in dicts, no-content or content attr
# smooth out extra content handling in Tag
# possibly nest the TagStreams?
# prepare vs render?  but there's no way to tell how many in the lists..


#### Main for standalone testing

if __name__ == '__main__':
    #from product.models import Category

    #lst = [] #Category.objects.filter (name__icontains='acc')
    #print TagItemList (lst, content_attr='name').li(cls='cat', d='slug').br.img(src='main_image', title='description').div.span.a(href='get_absolute_url')

    '''
    from apps.legacy.models import Product

    p = Product.objects.all() [0]



    #FormattedTagStream('product').h1('.title')
    pstream = ObjectTagStream().h1('name') \
        .p("Desc:{{ product.description or '(No Desc)' }}") \
        .p("Specs:{{ product.specs or '(No Specs)' }}") \
        .p.a('More Photos', href = '/photos/{{ product.slug }}') \
        .p('Base Price: {{ product.calc_baseprice|format:"$%.2f" }}') \
        .a(href='sku') \
        .render(p)

    print pstream


    #        .table(d='configgrid').treo.td(name).td(id).render (q)
    #    ('productoption_set.all')
    #        .td ...


    import sys
    sys.exit()
    '''

    class TestObj (object):
        name = "My Name"
        description = "My Description"
        url = "http://my/url.com"
        title = "My Title"
        slug = 'my_slug'

        nested = "This is a test this is only a test".split()
        nested2 = [dict(a=1,b=2,c=3) for i in range (5)]
        nested3 = dict(a=1,b=2,c=3)


    # Idea: Dictionary stack 7/9/11 JJW

    class AnotherTestObj (object):
        the_obj = TestObj
        nested = ObjectTagStreamBoth().li.render (the_obj.nested)
        _main = ObjectTagStreamBoth().div(cls='prod', d='%(slug)s123').br.img(src='url',
            title='eRacks: %(title)s').div('aha').span.a('description',
            href='/images/%(url)s').ul(cls='nested_list').li ('nested') # .render(the_obj)

        def render(self):
            print 'dict:', self.__dict__
            print
            print 'classdict:', self.__class__.__dict__
            print
            result = self._main.render (self.the_obj, **self.__class__.__dict__)


    print ObjectTagStreamBoth().div(cls='prod', d='%(slug)s123').br.img(src='url', title='eRacks: %(title)s').div('aha').span.a('description', href='/images/%(url)s').ul(cls='nested_list').li ('%(nested)s').render (TestObj)

    #print
    #print AnotherTestObj.__str__

    print
    print AnotherTestObj().render()

    import sys
    sys.exit()







    #for i in range (10000):
    ti = str(Wrap('{0.name}').li(cls='cat', d='{0.slug}').br.img(src='{0.main_image}', title='{0.description}').div('aha').span.a(href='{0.get_absolute_url}'))
    print ti

    ti = TagStream().li(cls='cat', d='{0.slug}').br.img(src='{0.main_image}', title='{0.description}').div('aha').span.a(href='{0.get_absolute_url}').render ('{0.name}')
    print ti


    print TagStream().li(cls='cat', d='{0.slug}').br.img(src='{0.main_image}', title='{0.description}').div('aha').span.a(href='{0.get_absolute_url}').render (TestObj.nested)

    print
    print ObjectTagStream().div(cls='prod', d='slug').br.img(src='url', title='title').div('aha').span.a('description', href='url').ul(cls='nested_list').li ('nested').render (TestObj)



#for o in Product.objects.filter (published=True):
#    what ?

# OK, I guess the way to go is to pass in the object, and always render with the given template mechanism - oldpy,
# newpy, django - and maybe conver the object to a disctionary for oldpy, or use a passed-in one. :(

    print
    print ObjectTagStream().div(cls='prod', d='%(slug)s').br.img(src='%(url)s', title='$(title)s').div('aha').span.a('%(description)s', href='%(url)s').ul(cls='nested_list').li ('%(nested)s').render (TestObj)

    print
    print ObjectTagStream2().div(cls='prod', d='%(slug)s').br.img(src='%(url)s', title='%(title)s').div('aha').span.a('%(description)s', href='%(url)s').ul(cls='nested_list').li ('%(nested)s').render (TestObj)

    print
    print ObjectTagStream3().div(cls='cat', d='${slug}ify!').br.img(src='$title}', title='$description$').div('$aha').span.a(href='$url').ul(cls="nested").li('$nested').render (TestObj)

    print
    print ObjectTagStream4().ol('{nested3}').ol('{nested2[0]}').div(cls='cat', d='{slug}').br.img(src='{title}', title='{description}').div('aha').span.a(href='{url}').ul(cls="nested").li('{nested}').render (TestObj)

    print
    print ObjectTagStream4().div(cls='cat', d='{0.slug}').br.img(src='{0.title}', title='{0.description}').div('aha').span.a(href='{0.url}').ul(cls="nested").li('{0.nested}').render (TestObj)

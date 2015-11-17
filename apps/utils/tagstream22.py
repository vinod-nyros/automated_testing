# tagstream22.py library Copyright (c) 2011-2012 Joseph J Wolff all rights reserved

# TODO 8/5/11: render_type, indent, tag_newline
# TODO 8/21/11 Cheboygan:  template, whole html page

# d TODO 4/27/12 loop (target=queryset), poss Formatter passed into init
# beta: simply pass iterable into the tag! :-D

# from string import Formatter


#### globals

trace = 0

# Set this to ' /' for xhtml-compliance
trailing_slash = ''

# html 4.01 / xhtml 1.0 single tag list - from http://www.w3schools.com/tags/default.asp
single_tags = ['area','base','basefont','br','col','frame','hr','img','input','link','meta','param',]

# Iterable test - strings are NOT iterable using this, which is exactly what we want
is_iterable = lambda x: hasattr (x, '__iter__')

# Shorten/avoid reserved words in keyword arguments - prepend / append with '_' also works
attrmap = lambda k: dict (
        cls='class',
        fr='for',
        d='id',
        http_equiv='http-equiv',
    ).get (k, k.strip ('_'))


### Classes

class Tag (object):
    def __init__ (self, tag='', trailing_slash=trailing_slash, **kw):
        self.tag = tag.lower()
        self.single_tag = self.tag in single_tags
        self.trailing_slash = trailing_slash
        self.kw = kw
        if trace: print self.tag

    def dict2attrs (self, kw):
        if kw:
            return ' ' + ' '.join (('='.join ((attrmap (k),'"%s"' % str(v))) for k,v in kw.items()))
        return ''

    def __repr__(self):
        return '<Tag instance: %s>' % self.tag

    def _emit (self, arg, **kw):
        if is_iterable (arg):
            return '\n'.join ([self._emit (content, **kw) for content in arg])

        # new 4/27/12 - check for iterable args, and iterate them!
        for k,v in kw.iteritems():
            if trace: print 'kv', k,v
            if is_iterable (v):
                kw.pop (k)  # remove it first
                # now set up render fn for keyword arguments
                renderkw = lambda kw, k, obj: dict ([(k2,v2.format (**{k:obj})) for k2,v2 in kw.iteritems()])
                # now render the list w/both args & kwargs
                return '\n'.join ([self._emit (arg.format (**{k:obj}), **renderkw(kw,k,obj)) for obj in v])

        if self.single_tag:
            return '%s<%s%s%s>\n' % (arg, self.tag, self.dict2attrs (kw), self.trailing_slash)
        else:
            return '<%s%s>%s</%s>\n' % (self.tag, self.dict2attrs (kw), arg, self.tag)

    def __call__ (self, *args, **kw):
        if trace: print args, kw
        return self._emit (args or '', **kw)



class NoTag (Tag):
    def __call__ (self, *args, **kw):
        raise Exception ('No Tag / Empty Tag cannot be called')


class CloseTag (object):  # note: not a descendant of Tag
    def __init__ (self, tag):
        toks = tag.lower().split ('_')

        if len (toks) == 2:
            self.tag = toks [-1]
        else:
            self.tag = '*'  # wildcard means close the first wrapping tag it finds

    def __repr__(self):
        return '<CloseTag instance: %s>' % self.tag


class TagStream (object):
    def __init__ (self):
        self.stack = []
        self._template = ''

    def __repr__(self):
        return '<TagStream instance: %s>' % ' '.join ([t.tag for t in self.stack if isinstance (t, Tag)])

    def _push (self, x):
        return self.stack.insert (0, x)
        #return self.stack.append (x)

    def __getattr__ (self, name):       # push Tag
        if name.lower().startswith('close'):
            self._push (CloseTag (name))
        else:
            self._push (Tag (name))

        return self  # chainable

    def __call__ (self, *args, **kw):   # push tuple - args, kw
        args = list (args)
        self._push ((args, kw))
        return self  # chainable

    def text (self, s):                 # push text (basestring)
        self._push (s)
        return self  # chainable


    # guaranteed a single item, not a list or *args
    # top down
    def new_render_item (self, itm, start=0):
        tag = NoTag()

        for i, x in enumerate (self.stack [start:]):
            if isinstance (x, Tag):
                tag = x
            elif isinstance (x, (str, unicode)):
                itm += x
            elif isinstance (x, CloseTag):
                itm += self._render_item ('', start = i+1, **kw)
            else:
                assert isinstance (x, tuple)
                args, kw = x
                if not args and not tag.single_tag:  # it's a wrap
                    itm += tag (self._render_item (itm, start=i+1), **kw)
                else:
                    itm += tag (*args, **kw)

        return itm

    # bottom up
    def _traverse(self):
        args, kw = [], {}
        itm, accum = '', []

        for x in self.stack:
            if isinstance (x, CloseTag):
                accum.append ([x,itm])
                itm = ''
            elif isinstance (x, (str, unicode)):  # same as basestring
                itm = x + itm
            elif isinstance (x, Tag):
                # if closing and close_tag.tag == x.tag):
                #     wrap the accumed items
                if not args and not x.single_tag:  # it's a wrap
                    itm = x (itm, **kw)  # so wrap it

                    if accum and accum [-1][0].tag in [x.tag, '*']:  # matches this tag, or is a wildcard
                       close_tag, popped_itm = accum.pop()
                       itm = itm + popped_itm
                else:
                    itm = x (*args, **kw) + itm  # prepend it
                args, kw = [], {}
            else:
                args, kw = x

        if trace: print 'ACCUM:', accum, '\n\n'
        return itm + '\n'.join ([s for (closetag,s) in accum])


    @property
    def template (self):
        if not self._template:
            self._template = self._traverse()  # traverse the stack, save the template

        return self._template


    def render (self, *args, **kw):  # pass in list of dicts, Django objects, anything with a dict, kw appended..
        if not args and not kw:
            return self.template

        ctx = {}

        for arg in args:
            #if isinstance (arg, (dict, dictproxy)):  # mapping_type?
            if isinstance (arg, dict):
                ctx.update (arg)
            elif hasattr (arg, '__dict__'):
                ctx.update (arg.__dict__)

        if kw:
            ctx.update (kw)

        if ctx:
            return self.template % ctx
        else:
            return self.template % (args or '')


    def render_list (self, the_list, **kw):
        return '\n'.join ([self.render (*dicts, **kw) for dicts in the_list])




#### Main for standalone testing

if __name__ == '__main__':

    class TestObj (object):
        name = "My Name"
        description = "My Description"
        url = "http://my/url.com"
        title = "My Title"
        slug = 'my_slug'

        nested = "This is a test this is only a test".split()
        nested2 = [dict(a=1,b=2,c=3) for i in range (5)]
        nested3 = dict(a=1,b=2,c=3)

    class TestObj2 (object):
        name = 'My SECOND name!'

    class X(object):
        pass

    prod1=X()
    prod1.name='Fred'
    prod1.url='fred.com'
    prod1.title='My Title'

    prod2=X()
    prod2.name='Klem'
    prod2.url='kadiddle.com'
    prod2.title='My Other Title'

    print (TagStream()
        .ul
            .il (prod=(prod1,prod2))
                .a ('{prod.name}', href='{prod.url}', title='{prod.title}')
            .close_li
            .div ('{prod.name}', prod=(prod1,prod2), title='{prod.title}')  # aha: title doesn't resolve..
        .template
    )

    import sys
    sys.exit()


    templet = (TagStream()
        .div ('name: %(name)s')
        .p ('desc: %(description)s', cls='green')
        .a ('a link to me', href='%(url)s')
        .img (title='The title: %(title)s', src='%(slug)s')
        .ul
            .li ('nested')
            .li ('nested2')
            .li ('nested3')
        .close
        .ul
            .li ('nested11', 'nested12', 'nested13')
        .close
        .ul
            .li
                .div
                    .a ('nested', href='/my/link')
                    .img (src='/my/img')
                    .text ('this is some text')
                    .span ('and a caption', _class='red')
            .close_li
            .li
                .div
                    .a ('nested2', href='/my/link2')
                    .img (src='/my/img2')
                    .text ('this is some text 2')
                    .span ('and a caption 2', _class='red')
            .close_li
            .li
                .div
                    .a ('nested3', href='/my/link3')
                    .img (src='/my/img3')
                    .text ('this is some text 3')
                    .span ('and a caption 3', _class='red')
            .close_li
        .close_ul
        .ul (d=3)
            .li ('nested4')
            .li ('nested5')
            .li ('nested6')
        #.close
        #.render()
    )

    if trace:
        from pprint import pprint
        pprint (templet.stack)

        print
        print templet
        print

    #print templet.template % TestObj.__dict__
    #print templet.render (TestObj)



    print (TagStream()
        .html
            .head
                .title ('The Libre Group - Web development, Technology, and Consulting')
                .meta (http_equiv='Content-Type', content='text/html; charset=UTF-8')
                .script (src='/static/js/jquery.js', _type='javascript')
                .link (href='/static/css/oocss.css', rel='stylesheet', _type='text/css')
            .close_head
            .body
                .div (cls='header')
                    .img (alt='libre logo', height=80, src='/static/images/logo.png')
                .close_div
                .div (cls='gradientbanner')
                    .div (cls='boxes')
            .close_body
        .template
    )




'''
Notes after St Joe's hill hike 7/23/11 ~3.5 - 4 mi:

- close & text can be string, pushed on stack
  - text could also be method, called w/text, but no kw's allowed
  - close just returns from recursive render call

- factory classes of Div, Span, etc

- try not to keep state, to avoid probs with:
    Div (Div ('aha).span('sothere'))...

- alternatively, use instantiated TagStreams, for div, span, etc, but then there might be a state prob w/nested usage
    - unless they all use the same one!

later in eve:

if close then
    tail = item
    item = ''

could also do item stack & join @end

- - -

    import inspect
    try:
        f = inspect.currentframe()
        print f
        print f.f_lineno
        print inspect.getframeinfo (f)
    finally:
        del f


- - -

    ts = TagStream()

    print (ts
        .div ('this is a div')
        .div ('this is a div 2')
        .div ('this is a div 3')
        .div ('this is a div 4')
        .ul
            .li ('my li').li('another li').li('yet a third li')
        .ul (d=2)
            .li ('my li').li('another li').li('yet a third li')
        .ul (d=3)
            .li ('my li').li('another li').li('yet a third li')
        .render('where')
    )

    print ('test: %(one)s %(two)s' % dict(one=1, two=2))

- - -

    templet = (Div(_class='container')
        .div ('name: %(name)s')
        .p ('desc: %(description)s', cls='green')
        .a ('a link to me', href='%(url)s') (Img (title='The title: %(title2)s', src='%(slug)s'))
        .ul
            .li ('nested','nested2','nested3')
        .ul (d=3)
            .li ('nested4')
            .li ('nested5')
            .li ('nested6')
        #.render()
    )


    print (ts
        .h1('hi')
        .div(
            ts.p ('So there.'),
            cls='green')
        .div(
            ts.span('Hello')
            .span ('world')
            .span ('My name is:')
            .span (TestObj.name)
        )
    )

    print ts.render()

    #TestObj = TestObj2
    #print ts.render()
    #print ts.stack  # Nope! call-by-value, not by-reference (or by name).  :-(

'''

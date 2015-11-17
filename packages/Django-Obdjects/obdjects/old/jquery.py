# coding: utf8
from inspect import isclass

from django.template import Context, Template
from django.template.defaultfilters import slugify

from eracks.obdjects.minitags import tr,td,a as link,p as para, ul,li,h1,h2,form,treo,table,tr,td,th,img,div,span,submit,hidden
from eracks.obdjects.classes import WebPage, WebSnippet, js_tags

trace = 0

class JQueryPage (WebPage):
  js = js_tags (['/js/jquery/jquery.js', '/js/jquery/jquery.ui.js'])
  #js =  js_tags (['js/jquery/jquery.ui.js','js/jquery/jquery-ui-personalized-1.5.3.js'])


class JQueryTabs (WebSnippet):  # assumes on a jquery page w/parent js - until we do the hash dict
  tab_color = '#CCCCFF'
  panel_color = 'white'
  css = '''
<style>
.ui-tabs-hide { display: none; } /* JJW !! */
.ui-tabs-nav {
  border-bottom: 1px solid black;
  margin-bottom: 0px;
}
.ui-tabs-nav li {
  list-style-type: none;
  display: inline;
  background-color: %(tab_color)s; /* lightblue; */
  border: 1px solid black;
  padding: 3px 10px 0 10px;
}
li.ui-tabs-selected, .ui-tabs-panel {
  background-color: %(panel_color)s; /* #efefef; CDCDCD; light gray */
}
li.ui-tabs-selected {
  /* border-bottom: 0; */
  border-bottom: 1px solid %(panel_color)s;
  padding-top: 5px;
  /* padding-bottom: 1px; */
  /* font-weight: bold; */
}
.ui-tabs-nav a:focus { border:none; outline:none; }
.ui-tabs-nav a:hover { text-decoration:none; }

</style>
''' # % dict (tab_color=tab_color, panel_color=panel_color)
  js = [js_tags ('/js/jquery/jquery-ui-tabs.js'),
        js_tags (txt='''
jQuery(document).ready(function(){
    jQuery("#%(name)s ul").tabs();
    jQuery("#addtab").click(function(){
        jQuery("#%(name)s ul").tabs('add', 'jqueryajaxtest', 'New Tab');
    });
});
''')] # % dict (name=self.name))

  #@property
  #def tabs (self):  # returns list of name/content pairs
  #  return ( ('One', 'this is the contents of tab one'),
  tabs =   ( ('One', 'this is the contents of tab one'),
             ('Two', 'this is the contents of tab two'),
             ('Three', 'this is the contents of tab three (<span id=addtab>add tab</span>)'),
           )

  def _prepare (self):
    namedict = dict (name = self._name)
    self.js = ''.join ([j % namedict for j in self.js])
    self.css = self.css % dict (tab_color=self.tab_color, panel_color=self.panel_color)
    return WebSnippet._prepare (self)


  def _render (self, req, ses, **parms):
    lst = ''
    divs = ''
    for tab, content in self.tabs:
      slug = slugify (tab)
      lst += li (link (span (tab), href='#%s' % slug))
      divs += div (content, d=slug)

    return div (ul(lst) + divs, d=self._name)


class JQuerySnippet (WebSnippet):  # assumes on a jquery page w/parent jquery js - until we do the hash dict
  def _prepare (self):
    namedict = dict (name = self._name)
    self.js = ''.join ([j % namedict for j in self.js])
    self.css = self.css % namedict

    return WebSnippet._prepare (self)


  def _render (self, req, ses, **parms):
    raise Exception, 'Subclass must implement "_render" method!'


class JQueryMenu (JQuerySnippet):  # assumes on a jquery page w/parent jquery js - until we do the hash dict
  css = '<style type="text/css">#%(name)s li { list-style-type:none; } #%(name)s li ul { display:none; }</style>'
  js = [#js_tags ('/js/jquery/jquery-ui-tabs.js'),
        js_tags (txt='''
jQuery(document).ready(function(){
    jQuery("#%(name)s li").click(function(){
        $(this).children('ul').toggle();
    });
    jQuery("#%(name)s a").click(function(event){
        //alert (this.href);
        event.preventDefault();
        $.ajax({
           method: "get",
           url: this.href, // "/ajax/%% (myid)s",
           //data: "page="+content_show,
           //beforeSend: function(){$("#loading").show("fast");}, //show loading just when link is clicked
           //complete: alert ('done'),
             //function(){ $("#loading").hide("fast");}, //stop showing loading when the process is complete
           success: function(html){ // alert (html);
             jQuery("#content").html (html) // should set to #id if id present else content
             //$(".content").show("slow"); //animation
             //$(".content").html(html); //show the html inside .content div
           },
           error: function (xhr, stat, err) {  // typically only one of textStatus or errorThrown will have info
             alert (stat + err);
             //this; // the options for this ajax request
           }
        });
    });
});
''')]


# Menu with nested lists - see recurse_for_children in Category model
class JQueryTreeMenu (JQuerySnippet):
  css = '''
<style type="text/css">
#%(name)s ul { list-style-type:none; list-style-position:inside;
		margin:0; white-space:nowrap; overflow:hidden; }
#%(name)s li ul { margin-left:7px; }
#%(name)s li.closed ul { display:none; }

#%(name)s li:before { content: url(/images/misc/bullet.png); margin-left: -3px; }
#%(name)s li.closed:before { content: url(/images/misc/triangle_right.png); }
#%(name)s li.open:before   { content: url(/images/misc/triangle_down.png); }

#%(name)s li a.current { font-weight: bold; }
</style>
<!--[if IE]><style type="text/css">
#%(name)s li, li.prod { list-style-image: url(/images/misc/bullet.png); }
#%(name)s li.closed { list-style-image: url(/images/misc/triangle_right.png); }
#%(name)s li.open { list-style-image: url(/images/misc/triangle_down.png); }
</style><![endif]-->
'''

  js = [#js_tags ('js/jquery/jquery-ui-tabs.js'),
        js_tags (txt='''
function getPath (url) {
  var a = url.split ('//')
  var r = a [a.length-1]
  return r.substr (r.indexOf ('/')+1)
}
jQuery(document).ready(function(){
    jQuery("#%(name)s li").click(function(e){
        $(this).children('ul').toggle();
        //$(this).nextAll('ul').toggle();
        $(this).toggleClass('closed');
        $(this).toggleClass('open');
        e.stopPropagation();
    });
    jQuery("#%(name)s a").click(function(event){
        // really need a list of valid pages, here, or check the first node of this.href
        //if (location.pathname.indexOf ('/product') < 0) // kluge alert!
        //  return;

        //event.preventDefault();  // stops from bubbling up to li parent
        event.stopPropagation();
        $('#%(name)s a.current').removeClass ('current')
        $(this).addClass ('current')
        /*
        var pathname = getPath (this.href);
        $.ajax({
           method: "get",
           url: this.href, // "/ajax/%% (myid)s",
           //data: "page="+content_show,
           //show loading just when link is clicked:
           //beforeSend: function(){$("#loading").show("fast");}, 
           //complete: alert ('done'),
             //stop showing loading when the process is complete
             //function(){ $("#loading").hide("fast");},

           //dataType: "none", none, nil, - nfg - "json"
           dataFilter: function (data, type) {
             //alert (type); - nope - nfg - undefined
             if (data [0] == '{')  // it's json, so eval it
               //alert ('yup');
               eval ('data = ' + data);
             // return the sanitized data
             return data;
           },

           success: function (data, stat) {
             //alert (typeof jso);
             if (typeof data == 'object')  // json obj w/key-value ids-html
               jQuery.each (data, function (k,v) {
                 //alert (k + ':' + v);
                 $("#" + k).html (v);
               })
             else // its plain html for this id
               $("#content").html (data);
             location.pathname = '#' + pathname;
           },

           //success: function(html){ // alert (html);
           //  jQuery("#content").html (html) // should set to #id if id present else content
           //  location.pathname = '#' + pathname;  // yuk; href reloads the same page again.
             //$(".content").show("slow"); //animation
             //$(".content").html(html); //show the html inside .content div
           //},

           error: function (xhr, stat, err) {
             // typically only one of textStatus or errorThrown will have info
             alert (stat + err);   //this; // the options for this ajax request
           }
        });
        */
    });
});
''')]



# = = = = =


decls = globals().items()[:]

for n,o in decls:
  if isclass (o) and issubclass (o, WebPage) and not o is WebPage:
    if trace: print 'NAME:', n.lower()
    globals() [n.lower()] = o()






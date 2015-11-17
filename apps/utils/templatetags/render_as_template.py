# -*- coding: utf-8 -*-

'''
from https://djangosnippets.org/snippets/1373/

This is a template tag that works like {% include %}, but instead of loading a template from a file, it uses some text from the current context, and renders that as though it were itself a template. This means, amongst other things, that you can use template tags and filters in database fields.

For example, instead of:

{{ flatpage.content }}

you could use:

{% render_as_template flatpage.content %}

Then you can use template tags (such as {% url showprofile user.id %}) in flat pages, stored in the database.

The template is rendered with the current context.

Warning - only allow trusted users to edit content that gets rendered with this tag.

Author: cogat
Posted: March 13, 2009
'''

from django import template
from django.template import Template, Variable, TemplateSyntaxError

register = template.Library()

class RenderAsTemplateNode(template.Node):
    def __init__(self, item_to_be_rendered):
        self.item_to_be_rendered = Variable(item_to_be_rendered)

    def render(self, context):
        try:
            actual_item = self.item_to_be_rendered.resolve(context)
            return Template(actual_item).render(context)
        except template.VariableDoesNotExist:
            return ''

def render_as_template(parser, token):
    bits = token.split_contents()
    if len(bits) !=2:
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (a variable representing a template to render)" % bits[0])
    return RenderAsTemplateNode(bits[1])

render_as_template = register.tag(render_as_template)

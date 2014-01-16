from django.template.base import Node, NodeList, TemplateSyntaxError
from django import template
from django.conf import settings

register = template.Library()


class IfInstalledNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, app, nodelist_true, nodelist_false, negate):
        self.app = app
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfInstalledNode>"

    def render(self, context):
        app = self.app.resolve(context, True)
        if (not self.negate and app in settings.INSTALLED_APPS) or \
           (self.negate and app not in settings.INSTALLED_APPS):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifinstalled(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    app = parser.compile_filter(bits[1])
    return IfInstalledNode(app, nodelist_true, nodelist_false, negate)


@register.tag
def ifinstalled(parser, token):
    """
    Outputs the contents of the block if the app is in settings.INSTALLED_APPS.

    Examples::

        {% ifinstalled 'bookmarks' %}
            ...
        {% endifinstalled %}

        {% ifnotinstalled 'bookmarks' %}
            ...
        {% else %}
            ...
        {% endifnotinstalled %}
    """
    return do_ifinstalled(parser, token, False)


@register.tag
def ifnotinstalled(parser, token):
    """
    Outputs the contents of the block if the app is not installed.
    See ifinstalled.
    """
    return do_ifinstalled(parser, token, True)

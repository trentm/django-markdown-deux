from django import template
from django.utils.safestring import mark_safe
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

import markdown_deux
from markdown_deux.conf import settings



register = template.Library()


@register.filter(name="markdown")
def markdown_filter(value, style="default"):
    """Processes the given value as Markdown, optionally using a particular
    Markdown style/config

    Syntax::

        {{ value|markdown }}            {# uses the "default" style #}
        {{ value|markdown:"mystyle" }}

    Markdown "styles" are defined by the `MARKDOWN_DEUX_STYLES` setting.
    """
    try:
        return mark_safe(markdown_deux.markdown(value, style))
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in `markdown` filter: "
                "The python-markdown2 library isn't installed.")
        return force_text(value)
markdown_filter.is_safe = True


@register.tag(name="markdown")
def markdown_tag(parser, token):
    nodelist = parser.parse(('endmarkdown',))
    bits = token.split_contents()
    if len(bits) == 1:
        style = "default"
    elif len(bits) == 2:
        style = bits[1]
    else:
        raise template.TemplateSyntaxError("`markdown` tag requires exactly "
            "zero or one arguments")
    parser.delete_first_token() # consume '{% endmarkdown %}'
    return MarkdownNode(style, nodelist)

class MarkdownNode(template.Node):
    def __init__(self, style, nodelist):
        self.style = style
        self.nodelist = nodelist
    def render(self, context):
        value = self.nodelist.render(context)
        try:
            return mark_safe(markdown_deux.markdown(value, self.style))
        except ImportError:
            if settings.DEBUG:
                raise template.TemplateSyntaxError("Error in `markdown` tag: "
                    "The python-markdown2 library isn't installed.")
            return force_text(value)


@register.inclusion_tag("markdown_deux/markdown_cheatsheet.html")
def markdown_cheatsheet():
    return {"help_url": settings.MARKDOWN_DEUX_HELP_URL}


@register.simple_tag
def markdown_allowed():
    return ('<a href="%s" target="_blank">Markdown syntax</a> allowed, but no raw HTML. '
        'Examples: **bold**, *italic*, indent 4 spaces for a code block.'
        % settings.MARKDOWN_DEUX_HELP_URL)



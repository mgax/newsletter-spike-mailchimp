import mrml
from django import template
from django.utils.safestring import mark_safe
from wagtail.rich_text import RichText

from spike.content.mjml_rendering import rewrite_db_html_for_email

register = template.Library()


@register.filter
def newsletter_richtext(value):
    if not isinstance(value, RichText):
        assert isinstance(value, str)
        value = RichText(value)

    return mark_safe(rewrite_db_html_for_email(value))


class MRMLRenderNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context) -> str:  # type: ignore
        mjml_source = self.nodelist.render(context)
        return mrml.to_html(mjml_source)  # type: ignore


@register.tag(name="mrml")
def mrml_tag(parser, token) -> MRMLRenderNode:
    """
    Compile MJML template after rendering the contents as a django template.

    Usage:
        {% mrml %}
            .. MJML template code ..
        {% endmrml %}
    """
    nodelist = parser.parse(('endmrml',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) != 1:
        raise template.TemplateSyntaxError(
            f"{tokens[0]!r} tag doesn't receive any arguments."
        )
    return MRMLRenderNode(nodelist)

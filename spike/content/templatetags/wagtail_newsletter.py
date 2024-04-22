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

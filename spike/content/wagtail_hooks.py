from wagtail import hooks
from wagtail.snippets.models import register_snippet

from . import viewsets
from .models import NewsletterAudience

register_snippet(NewsletterAudience)


@hooks.register("register_admin_viewset")  # type: ignore
def register_viewsets():
    return [
        viewsets.audience_chooser_viewset,
        viewsets.audience_segment_chooser_viewset,
    ]

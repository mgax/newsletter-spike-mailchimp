from django.db.models import CharField
from django.http import HttpResponse
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.rich_text import RichText

from . import mjml_rendering
from .viewsets import audience_chooser_viewset, audience_segment_chooser_viewset


class StandardPage(Page):
    body = RichTextField(
        features=[
            "bold",
            "italic",
            "code",
            "superscript",
            "subscript",
            "strikethrough",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ol",
            "ul",
            "blockquote",
            "link",
            "document-link",
            "image",
            "embed",
            "hr",
        ]
    )

    # TODO how long can these IDs be?
    newsletter_audience = CharField(max_length=1000, blank=True, null=True)
    newsletter_audience_segment = CharField(max_length=1000, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    newsletter_panels = [
        FieldPanel(
            "newsletter_audience",
            widget=audience_chooser_viewset.widget_class,
        ),
        FieldPanel(
            "newsletter_audience_segment",
            widget=audience_segment_chooser_viewset.widget_class(  # type: ignore
                linked_fields={"audience": "#id_newsletter_audience"},
            ),
        ),
    ]

    preview_modes = [  # type: ignore
        ("", "Default"),
        ("newsletter", "Newsletter"),
    ]

    def render_newsletter(self):
        return mjml_rendering.render(RichText(self.body))

    def serve_preview(self, request, mode_name):  # type: ignore
        if mode_name == "newsletter":
            return HttpResponse(self.render_newsletter().encode())
        else:
            return super().serve_preview(request, mode_name)

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(newsletter_panels, heading="Newsletter"),
        ],
    )

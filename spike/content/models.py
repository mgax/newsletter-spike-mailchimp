from django.http import HttpResponse
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.rich_text import RichText

from . import mjml_rendering


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

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    preview_modes = [  # type: ignore
        ('', 'Default'),
        ('newsletter', 'Newsletter'),
    ]

    def render_newsletter(self):
        return mjml_rendering.render(RichText(self.body))

    def serve_preview(self, request, mode_name):  # type: ignore
        if mode_name == "newsletter":
            return HttpResponse(self.render_newsletter().encode())
        else:
            return super().serve_preview(request, mode_name)

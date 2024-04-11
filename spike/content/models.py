from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


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

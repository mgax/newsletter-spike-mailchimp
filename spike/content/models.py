import mrml
from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy
from wagtail.admin.panels import FieldPanel, HelpPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.models import Page

from .viewsets import audience_chooser_viewset, audience_segment_chooser_viewset


class NewsletterAudience(models.Model):
    name = models.CharField(max_length=1000)
    audience_id = models.CharField(max_length=1000, blank=True, null=True)
    segment_id = models.CharField(max_length=1000, blank=True, null=True)

    panels = [
        FieldPanel("name"),
        FieldPanel(
            "audience_id",
            widget=audience_chooser_viewset.widget_class,
        ),
        FieldPanel(
            "segment_id",
            widget=audience_segment_chooser_viewset.widget_class(  # type: ignore
                linked_fields={"audience": "#id_audience_id"},
            ),
        ),
    ]

    def __str__(self):
        return self.name


class NewsletterPageMixin(Page):
    newsletter_audience = models.ForeignKey(
        NewsletterAudience, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:  # type: ignore
        abstract = True

    base_form_class: type
    content_panels: list
    promote_panels: list
    settings_panels: list

    newsletter_panels = [
        FieldPanel("newsletter_audience"),
        HelpPanel(content="Hello World"),
    ]

    preview_modes = [  # type: ignore
        ("", "Default"),
        ("newsletter", "Newsletter"),
    ]

    @classmethod
    def get_edit_handler(cls):
        tabs = []

        if cls.content_panels:
            tabs.append(ObjectList(cls.content_panels, heading=gettext_lazy("Content")))
        if cls.promote_panels:
            tabs.append(ObjectList(cls.promote_panels, heading=gettext_lazy("Promote")))
        if cls.settings_panels:
            tabs.append(
                ObjectList(cls.settings_panels, heading=gettext_lazy("Settings"))
            )

        tabs.append(
            ObjectList(cls.newsletter_panels, heading=gettext_lazy("Newsletter"))
        )

        edit_handler = TabbedInterface(tabs, base_form_class=cls.base_form_class)

        return edit_handler.bind_to_model(cls)

    newsletter_template: str

    def render_newsletter(self):
        return mrml.to_html(  # type: ignore
            render_to_string(self.newsletter_template, {"page": self})
        )

    def serve_preview(self, request, mode_name):  # type: ignore
        if mode_name == "newsletter":
            return HttpResponse(self.render_newsletter().encode())

        return super().serve_preview(request, mode_name)  # type: ignore


class StandardPage(NewsletterPageMixin, Page):  # type: ignore
    newsletter_template = "spike/content.mjml"

    body = RichTextField(features=settings.RICH_TEXT_FEATURES)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

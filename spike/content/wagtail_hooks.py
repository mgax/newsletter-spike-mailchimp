from wagtail import hooks

from . import viewsets


@hooks.register("register_admin_viewset")  # type: ignore
def register_viewsets():
    return [
        viewsets.audience_chooser_viewset,
        viewsets.audience_segment_chooser_viewset,
    ]

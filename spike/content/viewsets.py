from queryish import Queryish, VirtualModel
from wagtail.admin.viewsets.chooser import ChooserViewSet

from spike.mailchimp.client import get_client


class AudienceQuerySet(Queryish):
    def run_query(self):
        filters = dict(self.filters)
        client = get_client()
        audiences = client.lists.get_all_lists()["lists"]
        results = [
            Audience(
                pk=audience["id"],
                name=audience["name"],
                member_count=audience["stats"]["member_count"],
            )
            for audience in audiences
        ]
        for key, value in filters.items():
            if key == "pk":
                results = [result for result in results if str(result.pk) == value]
                if value and not results:
                    results = [Audience(value, "(deleted)", 0)]
            else:
                raise NotImplementedError(f"Unknown filter {key!r}")
        return results


class Audience(VirtualModel):
    base_query_class = AudienceQuerySet

    def __init__(self, pk, name, member_count):
        self.pk = pk
        self.name = name
        self.member_count = member_count

    def __str__(self):
        return f"{self.name} ({self.member_count})"

    class DoesNotExist(Exception):
        pass


class AudienceChooserViewSet(ChooserViewSet):
    model = Audience
    icon = "user"
    choose_one_text = "Choose an audience"
    choose_another_text = "Choose another audience"


audience_chooser_viewset = AudienceChooserViewSet("audience_chooser")


class AudienceSegmentQuerySet(Queryish):
    def run_query(self):
        filters = dict(self.filters)
        client = get_client()

        if "audience" in filters:
            audience = filters.pop("audience")
        elif "pk" in filters:
            audience = filters["pk"].split("/")[0]
        else:
            raise RuntimeError("Cannot determine audience ID")

        segments = client.lists.list_segments(audience)["segments"]
        results = [
            AudienceSegment(
                pk=f"{audience}/{segment['id']}",
                name=segment["name"],
                member_count=segment["member_count"],
            )
            for segment in segments
        ]
        for key, value in filters.items():
            if key == "pk":
                results = [result for result in results if str(result.pk) == value]
                if value and not results:
                    results = [Audience(value, "(deleted)", 0)]
            else:
                raise NotImplementedError(f"Unknown filter {key!r}")
        return results


class AudienceSegment(VirtualModel):
    base_query_class = AudienceSegmentQuerySet

    def __init__(self, pk, name, member_count):
        self.pk = pk
        self.name = name
        self.member_count = member_count

    def __str__(self):
        return f"{self.name} ({self.member_count})"

    class DoesNotExist(Exception):
        pass


class AudienceSegmentChooserViewSet(ChooserViewSet):
    model = AudienceSegment
    icon = "user"
    choose_one_text = "Choose an audience segment"
    choose_another_text = "Choose another audience segment"
    url_filter_parameters = ["audience"]
    preserve_url_parameters = ["multiple", "audience"]


audience_segment_chooser_viewset = AudienceSegmentChooserViewSet(
    "audience_segment_chooser"
)

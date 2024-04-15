from django.conf import settings
from django.core.cache import caches
from queryish import Queryish, VirtualModel
from wagtail.admin.viewsets.chooser import ChooserViewSet

from spike.mailchimp.client import get_client


class CachedApiQueryish(Queryish):
    def cache_key(self, pk: str) -> str:
        raise NotImplementedError

    def get_detail(self, pk: str) -> dict:
        raise NotImplementedError

    def get_list(self) -> dict[str, dict]:
        raise NotImplementedError

    def get_object(self, pk: str, **kwargs) -> VirtualModel:
        raise NotImplementedError

    def parse_filters(self):
        return dict(self.filters)

    def run_query(self):
        cache = caches["default"]
        filters = self.parse_filters()
        if set(filters) == {"pk"}:
            pk = filters["pk"]
            cache_key = self.cache_key(pk)
            kwargs = cache.get(cache_key)
            if kwargs is None:
                kwargs = self.get_detail(pk)
                cache.set(cache_key, kwargs, settings.NEWSLETTER_CACHE_TIMEOUT)
            yield self.get_object(pk, **kwargs)
            return

        if filters:
            raise RuntimeError(f"Filters not supported: {filters!r}")

        for pk, kwargs in self.get_list().items():
            cache.set(self.cache_key(pk), kwargs)
            yield self.get_object(pk, **kwargs)


class AudienceQuerySet(CachedApiQueryish):
    def get_object(self, pk, **kwargs):
        return Audience(pk=pk, **kwargs)

    def cache_key(self, pk):
        return f"newsletter-mailchimp-audience-{pk}"

    def get_detail(self, pk):
        client = get_client()
        audience = client.lists.get_list(pk)
        return {
            "name": audience["name"],
            "member_count": audience["stats"]["member_count"],
        }

    def get_list(self):
        client = get_client()
        audiences = client.lists.get_all_lists()["lists"]
        return {
            audience["id"]: {
                "name": audience["name"],
                "member_count": audience["stats"]["member_count"],
            }
            for audience in audiences
        }


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


class AudienceSegmentQuerySet(CachedApiQueryish):
    def get_object(self, pk, **kwargs):
        return AudienceSegment(pk=pk, **kwargs)

    def cache_key(self, pk):
        return f"newsletter-mailchimp-audience-segment-{pk}"

    def get_detail(self, pk):
        segment = self.get_list().get(pk, None)
        if segment is None:
            segment = {"name": "(deleted)", "member_count": 0}
        return segment

    def get_list(self):
        client = get_client()
        segments = client.lists.list_segments(self.audience_id)["segments"]
        return {
            f"{self.audience_id}/{segment['id']}": {
                "name": segment["name"],
                "member_count": segment["member_count"],
            }
            for segment in segments
        }

    def parse_filters(self):
        filters = super().parse_filters()

        if "audience" in filters:
            self.audience_id = filters.pop("audience")
        elif "pk" in filters:
            self.audience_id = filters["pk"].split("/")[0]
        else:
            raise RuntimeError("Cannot determine audience ID")

        return filters


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

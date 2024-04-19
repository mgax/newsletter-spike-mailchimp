from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Set campaign recipients"

    def add_arguments(self, parser):
        parser.add_argument("campaign_id")
        parser.add_argument("list_id")

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            result = client.campaigns.update(
                campaign_id=options["campaign_id"],
                body={
                    "recipients": {
                        "list_id": options["list_id"],
                    },
                },
            )
            pprint(result["recipients"])

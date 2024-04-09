from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_campaign, get_client, log_api_errors


class Command(BaseCommand):
    help = "Inspect a campaign"

    def add_arguments(self, parser):
        parser.add_argument("web_id", type=int)

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            campaign = get_campaign(client, options["web_id"])
            campaign.pop("_links")
            pprint(campaign)
            content = client.campaigns.get_content(campaign["id"])
            print(content["html"])

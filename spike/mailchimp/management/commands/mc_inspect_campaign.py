from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


def get_campaign(client, web_id):
    for campaign in client.campaigns.list()["campaigns"]:
        if campaign["web_id"] == web_id:
            return campaign

    raise KeyError("Campaign not found")


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

from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Inspect a campaign"

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            for campaign in client.campaigns.list()["campaigns"]:
                print("id:", campaign["id"])
                print("web_id:", campaign["web_id"])
                print("status:", campaign["status"])
                print("send_time:", campaign["send_time"])
                print()

                if options["verbosity"] > 1:
                    campaign.pop("_links")
                    pprint(campaign)
                    content = client.campaigns.get_content(campaign["id"])
                    print(content["html"])

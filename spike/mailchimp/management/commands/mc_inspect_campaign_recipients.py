from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Inspect campaign recipients"

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            for campaign in client.campaigns.list()["campaigns"]:
                print("## recipients")
                pprint(campaign["recipients"])
                print()

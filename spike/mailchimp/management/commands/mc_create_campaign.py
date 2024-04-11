from django.core.management.base import BaseCommand

from spike.content.mjml_rendering import render
from ...client import create_campaign, get_client, log_api_errors


class Command(BaseCommand):
    help = "Create a campaign"

    def add_arguments(self, parser):
        parser.add_argument("list_id")

    def handle(self, *args, **options):
        list_id = options["list_id"]
        client = get_client()
        with log_api_errors(reraise=False):
            campaign = create_campaign(client, recipients={"list_id": list_id})
            client.campaigns.set_content(campaign["id"], {"html": render()})
            print(campaign["id"])

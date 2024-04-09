from django.core.management.base import BaseCommand

from ...client import create_campaign, get_client, log_api_errors


class Command(BaseCommand):
    help = "Send a test email for a campaign"

    def add_arguments(self, parser):
        parser.add_argument("email")

    def handle(self, *args, **options):
        email = options["email"]
        client = get_client()
        with log_api_errors(reraise=False):
            campaign_id = create_campaign(client)["id"]
            try:
                client.campaigns.send_test_email(
                    campaign_id, {"test_emails": [email], "send_type": "html"}
                )
            finally:
                client.campaigns.remove(campaign_id)

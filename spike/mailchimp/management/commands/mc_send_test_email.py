from django.conf import settings
from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Send a test email for a campaign"

    def add_arguments(self, parser):
        parser.add_argument("campaign_id")

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            client.campaigns.send_test_email(
                options["campaign_id"],
                {
                    "test_emails": [settings.MAILCHIMP_TEST_ADDRESS],
                    "send_type": "html",
                },
            )

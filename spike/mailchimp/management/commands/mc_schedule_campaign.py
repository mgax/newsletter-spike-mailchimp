from datetime import UTC, datetime, timedelta
from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Schedule a campaign"

    def add_arguments(self, parser):
        parser.add_argument("campaign_id")
        parser.add_argument("seconds", type=int)

    def handle(self, *args, **options):
        client = get_client()
        time = datetime.now(UTC).replace(microsecond=0) + timedelta(
            seconds=options["seconds"]
        )
        with log_api_errors(reraise=False):
            client.campaigns.schedule(
                options["campaign_id"], {"schedule_time": time.isoformat()}
            )

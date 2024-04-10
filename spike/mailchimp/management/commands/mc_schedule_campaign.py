from datetime import UTC, datetime, timedelta
from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Schedule a campaign"

    def add_arguments(self, parser):
        parser.add_argument("campaign_id")

    def handle(self, *args, **options):
        client = get_client()
        time = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
        while time < datetime.now(UTC):
            time += timedelta(minutes=15)
        with log_api_errors(reraise=False):
            print(time)
            client.campaigns.schedule(
                options["campaign_id"], {"schedule_time": time.isoformat()}
            )

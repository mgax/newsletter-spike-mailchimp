from django.core.management.base import BaseCommand

from ...client import get_client


class Command(BaseCommand):
    help = "Ping the API"

    def handle(self, *args, **options):
        client = get_client()
        response = client.ping.get()
        print(response)

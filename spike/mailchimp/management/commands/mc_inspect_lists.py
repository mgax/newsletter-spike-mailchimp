from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Inspect the lists"

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            for mail_list in client.lists.get_all_lists()["lists"]:
                mail_list.pop("_links")
                pprint(mail_list)

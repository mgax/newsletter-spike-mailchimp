from pprint import pprint

from django.core.management.base import BaseCommand

from ...client import get_client, log_api_errors


class Command(BaseCommand):
    help = "Inspect the lists"

    def handle(self, *args, **options):
        client = get_client()
        with log_api_errors(reraise=False):
            for mail_list in client.lists.get_all_lists()["lists"]:
                print("id:", mail_list["id"])
                print("web_id:", mail_list["web_id"])
                print("stats['member_count']:", mail_list["stats"]["member_count"])
                print()

                if options["verbosity"] >= 2:
                    segments = client.lists.list_segments(mail_list["id"])["segments"]
                    if segments:
                        print("## segments")
                        for segment in segments:
                            segment.pop("_links")
                            pprint(segment)
                        print()

                if options["verbosity"] >= 3:
                    mail_list.pop("_links")
                    pprint(mail_list)
                    print()

from django.core.management.base import BaseCommand

from ...client import create_campaign, get_client, log_api_errors


class Command(BaseCommand):
    help = "Create a campaign"

    HTML = """
        <p>HELLO THERE <strong>html</strong>.</p>
        <p><a href="https://torchbox.com">click me!</a></p>
        <p><a href="*|UNSUB|*">unsubscribe</a></p>
    """

    def add_arguments(self, parser):
        parser.add_argument("list_id")

    def handle(self, *args, **options):
        list_id = options["list_id"]
        client = get_client()
        with log_api_errors(reraise=False):
            campaign = create_campaign(client, recipients={"list_id": list_id})
            client.campaigns.set_content(campaign["id"], {"html": self.HTML})
            print(campaign["id"])

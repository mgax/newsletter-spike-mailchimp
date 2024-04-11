from django.core.management.base import BaseCommand

from ...mjml_rendering import get_rich_text, render


class Command(BaseCommand):
    help = "Ping the API"

    def handle(self, *args, **options):
        rich_text = get_rich_text()
        print("## Rich text")
        print(rich_text)
        print()
        print("## Email text")
        print(render(str(rich_text)))

from django.conf import settings
from mailchimp_marketing import Client


def get_client():
    client = Client()
    client.set_config({"api_key": settings.MAILCHIMP_API_KEY})
    return client

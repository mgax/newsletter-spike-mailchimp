from contextlib import contextmanager
import logging
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger(__name__)


def get_client():
    client = Client()
    client.set_config({"api_key": settings.MAILCHIMP_API_KEY})
    return client


@contextmanager
def log_api_errors(reraise=True):
    try:
        yield
    except ApiClientError as error:
        logger.exception("Mailchimp API error: %s", error.text)
        if reraise:
            raise


def create_campaign(client):
    return client.campaigns.create(
        {
            "type": "regular",
            "settings": {
                "from_name": "Newsletter Spike",
                "reply_to": settings.MAILCHIMP_TEST_ADDRESS,
                "subject_line": "The Spike Campaign",
            },
        }
    )


def get_campaign(client, web_id):
    for campaign in client.campaigns.list()["campaigns"]:
        if campaign["web_id"] == web_id:
            return campaign

    raise KeyError("Campaign not found")

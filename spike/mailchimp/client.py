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


def create_campaign(client: Client, recipients=None):
    body = {
        "type": "regular",
        "settings": {
            "from_name": "Newsletter Spike",
            "reply_to": settings.MAILCHIMP_TEST_ADDRESS,
            "subject_line": "The Spike Campaign",
        },
    }
    if recipients:
        body["recipients"] = recipients

    return client.campaigns.create(body)

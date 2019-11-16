import requests
from requests.compat import urljoin
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


def get_user_by_email(email):
    max_pages = 10
    next_page = 1

    logger.debug("Constructing Harvest request")

    url = urljoin(settings.HARVEST_BASE_URL, "/v2/users")
    params = {"is_active": "true"}
    headers = {
        "Authorization": "Bearer {}".format(settings.HARVEST_ACCESS_TOKEN),
        "Harvest-Account-Id": settings.HARVEST_ACCOUNT_ID,
    }

    logger.debug("Constructed Harvest request")
    logger.info("Fetching Harvest users")

    while next_page is not None and next_page <= max_pages:
        r = requests.get(url, params={**params, "page": next_page}, headers=headers)

        if r.status_code != 200:
            logger.error("Harvest users could not be fetched")
            return None

        data = r.json()

        for user in data["users"]:
            if user["email"] == email:
                logger.info(
                    "Harvest user {} was found for email {}".format(user["id"], email)
                )
                return user

        next_page = data["next_page"]

    logger.warning("Harvest user was not found for email {}".format(email))
    return None

import logging
from huey.contrib.djhuey import db_task
from django.contrib.auth import get_user_model

from headway.harvest import get_user_by_email


logger = logging.getLogger(__name__)


@db_task()
def get_harvest_id_for_user(user_id):
    User = get_user_model()

    try:
        logger.debug("Fetching target user")

        user = User.objects.get(id=user_id)

        if user.email is None:
            logger.error("User could not be found")
            return None

        harvest_user = get_user_by_email(user.email)

        if harvest_user is None:
            logger.info("Harvest ID could not be found")
            return None

        harvest_id = harvest_user["id"]
        profile = user.profile
        profile.harvest_id = harvest_id
        profile.save()

        logger.info("Harvest ID {} was found for user {}".format(harvest_id, user_id))

        return harvest_id
    except Exception:
        logger.exception("User could not be found")
        return None

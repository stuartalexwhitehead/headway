import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from headway.models import Profile


logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="create_profile_for_user")
def create_profile_for_new_user(sender, **kwargs):
    user = kwargs.get("instance")
    created_user = kwargs.get("created")

    if not created_user:
        logger.debug("User is not new so skipping profile creation")
        return

    profile, created_profile = Profile.objects.get_or_create(user=user)

    logger.info("Got profile for user. Created: {}".format(created_profile))

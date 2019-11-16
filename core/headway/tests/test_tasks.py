from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest import mock

from headway.models import Profile
from headway.tasks import get_harvest_id_for_user


class GetHarvestIdForUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create(email="a@headway.com")
        cls.profile = Profile.objects.create(user=cls.user)

    def test_user_not_exist(self):
        task = get_harvest_id_for_user('7e546c57-91f3-4aa6-93d2-078f0e591517')
        result = task()

        self.assertIsNone(result)

    def test_harvest_id_not_found(self):
        with mock.patch('headway.tasks.get_user_by_email', return_value=None):
            task = get_harvest_id_for_user(self.user.id)
            result = task()

            self.assertIsNone(result)

    def test_harvest_id_found(self):
        ret = {"id": 12345}

        with mock.patch('headway.tasks.get_user_by_email', return_value=ret):
            task = get_harvest_id_for_user(self.user.id)
            result = task()

            self.profile.refresh_from_db()

            self.assertIsNotNone(result)
            self.assertEqual(result, ret["id"])
            self.assertEqual(self.profile.harvest_id, str(ret["id"]))
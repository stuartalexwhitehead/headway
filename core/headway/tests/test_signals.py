from django.test import TestCase
from django.contrib.auth import get_user_model


class CreateProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create(email="a@headway.com")

    def test_profile_created(self):
        print(self.user.profile)
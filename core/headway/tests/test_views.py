from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate

from headway.models import Profile, Feedback, FeedbackComment, FeedbackRequest
from headway.views import (
    ProfileView,
    FeedbackView,
    ReceivedFeedbackListView,
    SentFeedbackListView,
    FeedbackRequestView,
    ReceivedFeedbackRequestListView,
    SentFeedbackRequestListView,
    FeedbackCommentListView,
)


class ProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create()
        cls.factory = APIRequestFactory()

    def test_get_own_profile(self):
        request = self.factory.get("/api/v1/profile", format="json")
        force_authenticate(request, user=self.user)
        response = ProfileView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["receptiveness"], Profile.INDIFFERENT)

    def test_set_own_profile(self):
        invalid_request = self.factory.put(
            "/api/v1/profile", {"receptiveness": "nonsense"}, format="json"
        )
        force_authenticate(invalid_request, user=self.user)
        invalid_response = ProfileView.as_view()(invalid_request)

        self.assertEqual(invalid_response.status_code, 400)

        request = self.factory.put(
            "/api/v1/profile", {"receptiveness": Profile.SEEKING}, format="json"
        )
        force_authenticate(request, user=self.user)
        response = ProfileView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["receptiveness"], Profile.SEEKING)


class FeedbackTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.sender = User.objects.create(username="sender")
        cls.recipient = User.objects.create(username="recipient")
        cls.feedback = Feedback.objects.create(
            sender=cls.sender,
            recipient=cls.recipient,
            observation="One",
            impact="One",
            action="One",
        )
        cls.factory = APIRequestFactory()

    def test_get_received_feedback(self):
        recipient_request = self.factory.get(
            "/api/v1/feedback/received/", format="json"
        )
        force_authenticate(recipient_request, user=self.recipient)
        recipient_response = ReceivedFeedbackListView.as_view()(recipient_request)

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 1)

        sender_request = self.factory.get("/api/v1/feedback/received/", format="json")
        force_authenticate(sender_request, user=self.sender)
        sender_response = ReceivedFeedbackListView.as_view()(sender_request)

        self.assertEqual(sender_response.status_code, 200)
        self.assertEqual(len(sender_response.data), 0)

    def test_get_sent_feedback(self):
        sender_request = self.factory.get("/api/v1/feedback/sent/", format="json")
        force_authenticate(sender_request, user=self.sender)
        sender_response = SentFeedbackListView.as_view()(sender_request)

        self.assertEqual(sender_response.status_code, 200)
        self.assertEqual(len(sender_response.data), 1)

        recipient_request = self.factory.get("/api/v1/feedback/sent/", format="json")
        force_authenticate(recipient_request, user=self.recipient)
        recipient_response = SentFeedbackListView.as_view()(recipient_request)

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 0)

    def test_create_feedback(self):
        create_request = self.factory.post(
            "/api/v1/feedback/",
            {
                "recipient": self.recipient.id,
                "observation": "Two",
                "impact": "Two",
                "action": "Two",
            },
            format="json",
        )
        force_authenticate(create_request, user=self.sender)
        create_response = FeedbackView.as_view()(create_request)

        self.assertEqual(create_response.status_code, 201)

        recipient_request = self.factory.get(
            "/api/v1/feedback/received/", format="json"
        )
        force_authenticate(recipient_request, user=self.recipient)
        recipient_response = ReceivedFeedbackListView.as_view()(recipient_request)

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 2)
        self.assertEqual(recipient_response.data[0]["id"], create_response.data["id"])


class FeedbackRequestTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.sender = User.objects.create(username="sender")
        cls.recipient = User.objects.create(username="recipient")
        cls.feedback_request = FeedbackRequest.objects.create(
            type=FeedbackRequest.MANUAL, reason="One", sender=cls.sender
        )
        cls.feedback_request.recipients.add(cls.recipient)
        cls.factory = APIRequestFactory()

    def test_get_received_requests(self):
        recipient_request = self.factory.get(
            "/api/v1/requests/received/", format="json"
        )
        force_authenticate(recipient_request, user=self.recipient)
        recipient_response = ReceivedFeedbackRequestListView.as_view()(
            recipient_request
        )

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 1)

        sender_request = self.factory.get("/api/v1/requests/received/", format="json")
        force_authenticate(sender_request, user=self.sender)
        sender_response = ReceivedFeedbackRequestListView.as_view()(sender_request)

        self.assertEqual(sender_response.status_code, 200)
        self.assertEqual(len(sender_response.data), 0)

    def test_get_sent_requests(self):
        sender_request = self.factory.get("/api/v1/requests/sent/", format="json")
        force_authenticate(sender_request, user=self.sender)
        sender_response = SentFeedbackRequestListView.as_view()(sender_request)

        self.assertEqual(sender_response.status_code, 200)
        self.assertEqual(len(sender_response.data), 1)

        recipient_request = self.factory.get("/api/v1/requests/sent/", format="json")
        force_authenticate(recipient_request, user=self.recipient)
        recipient_response = SentFeedbackRequestListView.as_view()(recipient_request)

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 0)

    def test_create_request(self):
        create_request = self.factory.post(
            "/api/v1/requests/",
            {
                "type": FeedbackRequest.MANUAL,
                "reason": "Two",
                "recipients": [self.recipient.id],
            },
            format="json",
        )
        force_authenticate(create_request, user=self.sender)
        create_response = FeedbackRequestView.as_view()(create_request)

        self.assertEqual(create_response.status_code, 201)

        recipient_request = self.factory.get(
            "/api/v1/requests/received/", format="json"
        )
        force_authenticate(recipient_request, user=self.recipient)
        recipient_response = ReceivedFeedbackRequestListView.as_view()(
            recipient_request
        )

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 2)
        self.assertEqual(recipient_response.data[0]["id"], create_response.data["id"])


class FeedbackCommentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user_1 = User.objects.create(username="user-1")
        cls.user_2 = User.objects.create(username="user-2")
        cls.user_3 = User.objects.create(username="user-3")

        cls.feedback = Feedback.objects.create(
            sender=cls.user_1,
            recipient=cls.user_2,
            observation="One",
            impact="One",
            action="One",
            is_anonymous=True,
        )

        cls.feedback_comment = FeedbackComment.objects.create(
            feedback=cls.feedback, message="Message One", sender=cls.user_2
        )

        cls.factory = APIRequestFactory()

        cls.url = "/api/v1/feedback/{}/comment/".format(cls.feedback.id)

    def test_get_comments(self):
        sender_request = self.factory.get(self.url, format="json")
        force_authenticate(sender_request, user=self.user_1)
        sender_response = FeedbackCommentListView.as_view()(
            sender_request, feedback_id=str(self.feedback.id)
        )

        self.assertEqual(sender_response.status_code, 200)
        self.assertEqual(len(sender_response.data), 1)
        self.assertEqual(sender_response.data[0]["sender"], self.user_2.id)

        recipient_request = self.factory.get(self.url, format="json")
        force_authenticate(recipient_request, user=self.user_2)
        recipient_response = FeedbackCommentListView.as_view()(
            recipient_request, feedback_id=str(self.feedback.id)
        )

        self.assertEqual(recipient_response.status_code, 200)
        self.assertEqual(len(recipient_response.data), 1)
        self.assertEqual(sender_response.data[0]["sender"], self.user_2.id)

        nosey_parker_request = self.factory.get(self.url, format="json")
        force_authenticate(nosey_parker_request, user=self.user_3)
        nosey_parker_response = FeedbackCommentListView.as_view()(
            nosey_parker_request, feedback_id=str(self.feedback.id)
        )

        self.assertEqual(nosey_parker_response.status_code, 403)

    def test_create_comment(self):
        create_request = self.factory.post(
            self.url, {"message": "Message 2"}, format="json"
        )
        force_authenticate(create_request, user=self.user_1)
        create_response = FeedbackCommentListView.as_view()(
            create_request, feedback_id=str(self.feedback.id)
        )

        self.assertEqual(create_response.status_code, 201)

        complete_chancer_request = self.factory.post(
            self.url, {"message": "Message 3"}, format="json"
        )
        force_authenticate(complete_chancer_request, user=self.user_3)
        complete_chancer_response = FeedbackCommentListView.as_view()(
            complete_chancer_request, feedback_id=str(self.feedback.id)
        )

        self.assertEqual(complete_chancer_response.status_code, 403)

        get_request = self.factory.get(self.url, format="json")
        force_authenticate(get_request, user=self.user_2)
        get_response = FeedbackCommentListView.as_view()(
            get_request, feedback_id=str(self.feedback.id)
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.data), 2)
        self.assertEqual(get_response.data[1]["sender"], "Anonymous")

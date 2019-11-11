from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from headway.models import Profile, Feedback, FeedbackComment, FeedbackRequest
from headway.serializers import (
    ProfileSerializer,
    FeedbackSerializer,
    FeedbackCommentSerializer,
    FeedbackRequestSerializer,
)
from headway.permissions import FeedbackCommentMemberPermission


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        obj = get_object_or_404(queryset, user=user)
        self.check_object_permissions(self.request, obj)
        return obj


class FeedbackView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        return user.sent_feedback.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ReceivedFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        return user.received_feedback.order_by("-created").all()


class SentFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        return user.sent_feedback.order_by("-created").all()


class FeedbackCommentListView(generics.ListCreateAPIView):
    # TODO: hide sender when feedback is anonymous

    serializer_class = FeedbackCommentSerializer
    permission_classes = [IsAuthenticated, FeedbackCommentMemberPermission]

    def get_queryset(self):
        feedback_id = self.kwargs["feedback_id"]
        return (
            FeedbackComment.objects.select_related("feedback")
            .filter(feedback__id=feedback_id)
            .all()
        )

    def perform_create(self, serializer):
        user = self.request.user
        feedback_id = self.kwargs["feedback_id"]
        queryset = Feedback.objects.all()
        feedback = get_object_or_404(queryset, id=feedback_id)

        serializer.save(sender=user, feedback=feedback)


class FeedbackRequestView(generics.CreateAPIView):
    serializer_class = FeedbackRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return user.sent_feedback_requests.all()


class ReceivedFeedbackRequestListView(generics.ListAPIView):
    serializer_class = FeedbackRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return user.received_feedback_requests.order_by("-created").all()


class SentFeedbackRequestListView(generics.ListAPIView):
    serializer_class = FeedbackRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return user.sent_feedback_requests.order_by("-created").all()


# TODO: cancel feedback request

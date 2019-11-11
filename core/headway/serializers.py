from django.contrib.auth import get_user_model
from rest_framework import serializers

from headway.models import Profile, Feedback, FeedbackComment, FeedbackRequest


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "receptiveness"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "id",
            "is_read",
            "is_anonymous",
            "recipient",
            "sender",
            "feedback_request",
            "observation",
            "impact",
            "action",
            "created",
            "updated",
        ]

        # read_only so we can set sender after serializer validation
        # see https://stackoverflow.com/questions/27337519/django-rest-framework-what-is-the-equivalent-of-perform-create-in-apiview
        read_only_fields = ["sender"]


class FeedbackCommentSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    def get_sender(self, obj):
        if obj.feedback.is_anonymous and obj.sender.id == obj.feedback.sender.id:
            return "Anonymous"
        else:
            return obj.sender.id

    class Meta:
        model = FeedbackComment
        fields = [
            "id",
            "is_read",
            "message",
            "feedback",
            "created",
            "updated",
            "sender",
        ]
        read_only_fields = ["feedback"]


class FeedbackRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackRequest
        fields = [
            "id",
            "type",
            "status",
            "reason",
            "sender",
            "recipients",
            "created",
            "updated",
        ]
        read_only_fields = ["sender"]

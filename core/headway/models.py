import uuid

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TrackedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, UUIDModel):
    pass


class Profile(UUIDModel):
    SEEKING = "SEEKING"
    INDIFFERENT = "NEUTRAL"
    NOT_SEEKING = "NOT_SEEKING"

    RECEPTIVENESS_CHOICES = [
        (SEEKING, "Actively seeking feedback"),
        (INDIFFERENT, "Indifferent to feedback"),
        (NOT_SEEKING, "Prefer no feedback"),
    ]

    receptiveness = models.CharField(
        choices=RECEPTIVENESS_CHOICES, default=INDIFFERENT, max_length=11
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False
    )


class Feedback(UUIDModel, TrackedModel):
    is_read = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_feedback",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="sent_feedback",
    )
    feedback_request = models.ForeignKey(
        "FeedbackRequest", on_delete=models.SET_NULL, null=True, blank=True
    )
    observation = models.TextField()
    impact = models.TextField()
    action = models.TextField()


class FeedbackComment(UUIDModel, TrackedModel):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    feedback = models.ForeignKey("Feedback", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )


class FeedbackRequest(UUIDModel, TrackedModel):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"

    REQUEST_TYPE_CHOICES = [
        (MANUAL, "Manual request"),
        (SCHEDULED, "Scheduled request"),
    ]

    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [(ACTIVE, "Active"), (CANCELLED, "Cancelled")]

    type = models.CharField(choices=REQUEST_TYPE_CHOICES, max_length=9)
    status = models.CharField(choices=STATUS_CHOICES, default=ACTIVE, max_length=9)
    reason = models.TextField()
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="received_feedback_requests"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_feedback_requests",
    )

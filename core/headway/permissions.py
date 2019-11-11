from django.shortcuts import get_object_or_404
from rest_framework import permissions

from headway.models import Feedback


class FeedbackCommentMemberPermission(permissions.BasePermission):
    message = "You must have requested or sent feedback in order to add comments"

    def has_permission(self, request, view):
        queryset = Feedback.objects.all()
        feedback_id = view.kwargs["feedback_id"]
        obj = get_object_or_404(queryset, id=feedback_id)

        return obj.sender == request.user or obj.recipient == request.user

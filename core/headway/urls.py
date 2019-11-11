from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url

from headway.views import (
    ProfileView,
    FeedbackView,
    ReceivedFeedbackListView,
    SentFeedbackListView,
    FeedbackCommentListView,
    FeedbackRequestView,
    ReceivedFeedbackRequestListView,
    SentFeedbackRequestListView,
)


devpatterns = [url(r"^api-auth/", include("rest_framework.urls"))]

prodpatterns = [
    path("admin/", admin.site.urls),
    # see https://github.com/RealmTeam/django-rest-framework-social-oauth2#installation
    url("auth/", include("social_django.urls", namespace="social")),
    # see https://github.com/st4lk/django-rest-social-auth#quick-start
    url(r"^api/login/", include("rest_social_auth.urls_token")),
    # headway API views
    url(r"^api/v1/profile/", ProfileView.as_view()),
    url(r"^api/v1/feedback/", FeedbackView.as_view()),
    url(r"^api/v1/feedback/received/", ReceivedFeedbackListView.as_view()),
    url(r"^api/v1/feedback/sent/", SentFeedbackListView.as_view()),
    url(
        r"^api/v1/feedback/(?P<feedback_id>.+)/comments/",
        FeedbackCommentListView.as_view(),
    ),
    url(r"^api/v1/requests/", FeedbackRequestView.as_view()),
    url(r"^api/v1/requests/received/", ReceivedFeedbackRequestListView.as_view()),
    url(r"^api/v1/requests/sent/", SentFeedbackRequestListView.as_view()),
]


urlpatterns = [*prodpatterns, *devpatterns] if settings.DEBUG else [*prodpatterns]

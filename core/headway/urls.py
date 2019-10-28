from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url


devpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
]

prodpatterns = [
    path('admin/', admin.site.urls),

    # see https://github.com/RealmTeam/django-rest-framework-social-oauth2#installation
    url('auth/', include('social_django.urls', namespace='social')),

    # see https://github.com/st4lk/django-rest-social-auth#quick-start
    url(r'^api/login/', include('rest_social_auth.urls_token')),
]


urlpatterns = [*prodpatterns, *devpatterns] if settings.DEBUG else [*prodpatterns]

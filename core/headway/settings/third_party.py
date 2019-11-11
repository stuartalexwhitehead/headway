import environ


env = environ.Env()

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# see https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OPENID_WHITELISTED_DOMAINS = env.list('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS', default=[])

REST_SOCIAL_OAUTH_REDIRECT_URI = env.str('REST_SOCIAL_OAUTH_REDIRECT_URI')

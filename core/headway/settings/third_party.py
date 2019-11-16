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

HUEY = {
    'immediate': env.bool('HUEY_IMMEDIATE'),
    'connection': {
        'url': env.str('HUEY_REDIS_URL'),
    },
    'consumer': {
        'workers': 2,
    },
}

SHELL_PLUS_PRE_IMPORTS = [
    ('headway.harvest', '*'),
    ('headway.tasks', '*'),
]

HARVEST_BASE_URL = "https://api.harvestapp.com"
FORECAST_BASE_URL = "https://api.forecastapp.com"
HARVEST_ACCESS_TOKEN = env.str('HARVEST_ACCESS_TOKEN')
HARVEST_ACCOUNT_ID = env.str('HARVEST_ACCOUNT_ID')
FORECAST_ACCOUNT_ID = env.str('FORECAST_ACCOUNT_ID')

# see https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OPENID_WHITELISTED_DOMAINS = env.list('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS', default=[])

REST_SOCIAL_OAUTH_REDIRECT_URI = env.str('REST_SOCIAL_OAUTH_REDIRECT_URI')

from django.apps import AppConfig


class HeadwayAppConfig(AppConfig):
    name = "headway"

    def ready(self):
        import headway.signals

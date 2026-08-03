from django.apps import AppConfig


class SheltersConfig(AppConfig):
    name = "apps.shelters"

    def ready(self):
        import apps.shelters.signals  # noqa: F401

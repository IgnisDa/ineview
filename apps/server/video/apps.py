import os

from django.apps import AppConfig
from django.conf import settings


class VideoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "video"

    def ready(self):
        from .jobs import start_scheduler

        if os.environ.get("RUN_MAIN", None) != "true" and not settings.DEBUG:
            start_scheduler()

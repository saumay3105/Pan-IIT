import os
from django.apps import AppConfig

from django.conf import settings


class VideoGeneratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "video_generator"

    def ready(self):
        if not os.path.exists(settings.UPLOADED_DOCUMENTS_FOLDER):
            os.makedirs(settings.UPLOADED_DOCUMENTS_FOLDER)

        if not os.path.exists(settings.GENERATED_VIDEOS_FOLDER):
            os.makedirs(settings.GENERATED_VIDEOS_FOLDER)

        if not os.path.exists(settings.TEMPORARY_ASSETS_FOLDER):
            os.makedirs(settings.TEMPORARY_ASSETS_FOLDER)

        if not os.path.exists(settings.LOG_DIR):
            os.makedirs(settings.LOG_DIR)

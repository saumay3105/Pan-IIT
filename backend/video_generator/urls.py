from django.urls import path
from . import views

urlpatterns = [
    path(
        "generate-video/",
        views.generate_video,
    ),
    path(
        "video-status/<uuid:video_job_id>/",
        views.check_video_generation_status,
    ),
    path(
        "publish-video/<uuid:video_id>/",
        views.publish_video,
    ),
    path(
        "video/<uuid:video_id>/",
        views.get_video,
    ),
    path(
        "video/all/",
        views.get_all_published_videos,
    ),
    path(
        "answer/",
        views.answer_question,
    ),
    path(
        "tts/",
        views.get_tts,
    ),
]

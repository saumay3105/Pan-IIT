from datetime import timedelta
import os
import json
import uuid
import asyncio
import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from moviepy.editor import VideoFileClip

from .models import VideoProcessingJob, Video
from .functionalities.text_processing import (
    generate_script,
)
from .functionalities.video_synthesis import (
    generate_speech_and_viseme_from_text,
    generate_thumbnail,
    generate_video_details,
    generate_video_from_script,
)


@shared_task
def generate_script_task(
    job_id: uuid.UUID, video_preference: str, language: str, text: str = None
):
    job = VideoProcessingJob.objects.get(job_id=job_id)
    job.status = "processing"
    job.save()

    try:
        if text:
            script = generate_script(
                text=text, video_preference=video_preference, language=language
            )
        else:
            file_path = job.file.path
            script = generate_script(
                file_path=file_path,
                video_preference=video_preference,
                language=language,
            )

        job.script = script

    except Exception as e:
        job.status = "failed"
        job.script = None
        logging.error("Error generating script: %s", {str(e)})

    finally:
        job.save()


@shared_task
def process_video_task(video_job_id):
    try:
        video_job = VideoProcessingJob.objects.get(job_id=video_job_id)
    except ObjectDoesNotExist:
        return {
            "status": "error",
            "job_id": str(video_job_id),
            "message": f"No VideoProcessingJob found with id {video_job_id}",
        }

    # Set up paths to save audio and video
    audio_output_file = os.path.join(
        settings.MEDIA_ROOT, "temp_asset", f"{video_job_id}.wav"
    )
    video_output_file = os.path.join(
        settings.MEDIA_ROOT, "generated_videos", f"{video_job_id}.mp4"
    )

    # Ensure the temp_asset directory exists
    os.makedirs(os.path.dirname(audio_output_file), exist_ok=True)

    try:
        visemes = generate_speech_and_viseme_from_text(
            text=video_job.script, audio_output_file=audio_output_file
        )

        asyncio.run(
            generate_video_from_script(
                script=video_job.script,
                audio_output_file=audio_output_file,
                video_output_file=video_output_file,
            )
        )

        if os.path.exists(video_output_file):
            video_id = uuid.uuid4()
            try:
                video_details = generate_video_details(video_job)
                video_details = json.loads(video_details)
            except Exception:
                video_details = {}

            video_clip = VideoFileClip(video_output_file)
            video_duration = video_clip.duration
            thumbnail_output = os.path.join(
                settings.MEDIA_ROOT, "thumbnails", f"{video_job_id}.jpg"
            )
            os.makedirs(os.path.dirname(thumbnail_output), exist_ok=True)

            # Create video instance with video duration and thumbnail
            generate_thumbnail(video_clip, video_duration, thumbnail_output)

            video = Video.objects.create(
                video_id=video_id,
                video_job=video_job,
                title=video_details.get("title", ""),
                description=video_details.get("description", ""),
                video_file=os.path.join("generated_videos", f"{video_job_id}.mp4"),
                thumbnail=thumbnail_output,
                visemes=visemes,
                duration=timedelta(seconds=video_duration),
            )
            video_job.status = "completed"
            video_job.file = os.path.join("generated_videos", f"{video_job_id}.mp4")

    except Exception as e:
        video_job.status = "failed"
        logging.error("Error generating video: %s", {str(e)})

    finally:
        video_job.save()

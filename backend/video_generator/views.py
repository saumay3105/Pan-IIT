import logging
import os
import uuid
from datetime import timedelta
import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from celery import chain
from .functionalities.video_synthesis import (
    generate_speech_and_viseme_from_text,
)
from .functionalities.text_processing import generate_answer_from_question
from .models import VideoProcessingJob, Video
from .tasks import generate_script_task, process_video_task, send_emails_to_target


@api_view(["POST"])
def generate_video(request: HttpRequest):
    file = request.FILES.get("file")
    text = request.data.get("text")
    video_preference = request.data.get("video_preference")
    language = request.data.get("language")

    # Validate input
    accepted_formats = [".pdf", ".doc", ".docx", ".pptx", ".jpg", ".jpeg", ".png"]
    if file and not any(file.name.endswith(ext) for ext in accepted_formats):
        return Response(
            {
                "status": "error",
                "message": f"Invalid file format. Please provide a valid document. Accepted formats are: {', '.join(accepted_formats)}",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    SUPPORTED_LANGUAGES = [
        "English",
        "Hindi",
        "Tamil",
        "Telugu",
        "Kannada",
        "Malayalam",
        "Marathi",
        "Punjabi",
        "Urdu",
        "Gujrati",
    ]
    if language not in SUPPORTED_LANGUAGES:
        return Response(
            {
                "status": "error",
                "message": f"Invalid language selection. Supported languages: {', '.join(SUPPORTED_LANGUAGES)}",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Create a unique job ID for this process
        job_id = uuid.uuid4()

        # Save the job details to the database (initial status: queued)
        processing_job = VideoProcessingJob.objects.create(
            job_id=job_id,
            file=file if file else None,
            status="queued",
            video_preference=video_preference,
            language=language,
        )

        # Trigger a chain of asynchronous Celery tasks
        chain(
            generate_script_task.s(
                job_id=processing_job.job_id,
                video_preference=video_preference,
                language=language,
                text=text,
            ),
            process_video_task.si(processing_job.job_id),
            send_emails_to_target.si(processing_job.job_id),
        ).apply_async()

        return Response(
            {
                "status": "success",
                "message": "Document uploaded successfully. Processing started.",
                "job_id": job_id,
            },
            status=status.HTTP_202_ACCEPTED,
        )

    except Exception as e:
        logging.error("Error processing upload: %s", {str(e)})
        return Response(
            {
                "status": "error",
                "message": "An error occurred while processing the document.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def check_video_generation_status(request, video_job_id):
    try:
        video_job = VideoProcessingJob.objects.get(job_id=video_job_id)

        if video_job.status == "completed":
            video = Video.objects.get(video_job=video_job)
            return Response(
                {
                    "status": video_job.status,
                    "videoId": video.video_id,
                },
                status=status.HTTP_200_OK,
            )

        return Response({"status": video_job.status}, status=status.HTTP_200_OK)

    except VideoProcessingJob.DoesNotExist:
        return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

    except Video.DoesNotExist:
        return Response(
            {"error": "Video not found for the job."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def publish_video(request, video_id):
    try:
        # Fetch the video processing job
        video = Video.objects.get(video_id=video_id)
        video.published = True
        video.save()

        return Response(
            {
                "status": "success",
                "message": "Video published successfully.",
            },
            status=status.HTTP_200_OK,
        )

    except Video.DoesNotExist:
        return Response(
            {"error": "Video job not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logging.error("Error publishing video: %s", e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_video(request, video_id):
    try:
        video = Video.objects.get(video_id=video_id)

        video_data = {
            "video_id": str(video.video_id),  # Ensure UUID is converted to string
            "title": video.title,
            "description": video.description,
            "video_file": str(video.video_file.url),  # Convert to string
            "thumbnail": (
                str(video.thumbnail.url) if video.thumbnail else None
            ),  # Handle thumbnail as URL or None
            "visemes": video.visemes,
            "duration": video.duration.total_seconds(),  # Convert timedelta to seconds
            "created_at": video.created_at.isoformat(),  # Ensure datetime is serialized as ISO format
        }

        return Response({"video": video_data}, status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        return Response(
            {"error": "Video not found or is not published."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logging.error("Error fetching video: %s", e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_all_published_videos(request):
    try:
        # Get all published videos
        videos = Video.objects.filter(published=True)

        # Create a list of video data dictionaries
        videos_data = [
            {
                "video_id": str(video.video_id),  # Ensure UUID is converted to string
                "title": video.title,
                "description": video.description,
                "video_file": str(video.video_file.url),  # Convert to string
                "thumbnail": (
                    str(video.thumbnail.url) if video.thumbnail else None
                ),  # Handle thumbnail as URL or None
                "duration": video.duration.total_seconds(),  # Convert timedelta to seconds
                "created_at": video.created_at.isoformat(),  # Ensure datetime is serialized as ISO format
            }
            for video in videos
        ]

        return Response({"videos": videos_data}, status=status.HTTP_200_OK)

    except Exception as e:
        logging.error("Error fetching videos: %s", e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def answer_question(request):
    question = request.data.get("question")
    speech = request.data.get("speech")

    if not question:
        return Response(
            {"error": "'question' is required"},
            status=400,
        )

    answer = generate_answer_from_question(question=question, speech=speech)

    return Response({"answer": answer}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_tts(request: HttpRequest):
    text = request.data.get("text")
    teacher = request.data.get("teacher")

    audio_output_file = os.path.join(
        settings.MEDIA_ROOT, "temp_assets", f"{uuid.uuid4()}.wav"
    )
    try:
        visemes = generate_speech_and_viseme_from_text(
            text=text, audio_output_file=audio_output_file, voice=teacher
        )

        with open(audio_output_file, "rb") as audio_file:
            if audio_file is None:
                return Response(
                    {"error": "Text-to-speech synthesis failed"}, status=500
                )

            response = HttpResponse(audio_file.read(), content_type="audio/wav")

            # Set headers for the response
            response["Content-Disposition"] = "inline; filename=tts.wav"
            response["visemes"] = json.dumps(
                visemes
            )  # Include the viseme data as JSON in a header

        return response
    finally:
        # Clean up temporary file
        if os.path.exists(audio_output_file):
            os.remove(audio_output_file)

from itertools import islice
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from video_generator.models import VideoProcessingJob
from core.tasks import generate_image_posts
from core.utils.instagram_utils import generate_caption, post_on_insta
from core.utils.scraping_utils import extract_page
from core.utils.text_processing import get_product_info
from core.utils.whatsapp_utils import send_whatsapp_message
import csv
import cv2
import os
import base64
from io import BytesIO
from PIL import Image
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from .upload_video import upload_video_to_youtube
from email.mime.image import MIMEImage


def get_caption(content):
    trends = extract_page()
    content = "The post is about new financial scheme by Bajaj finserv introduced for students to help them pursure their degree by providing financial aid."
    caption = generate_caption(trends, content)

    return caption


@api_view(["POST", "GET"])
def create_posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        job_id = data.get("job_id")
        generate_image_posts.delay(data.get("job_id"))
        return Response({"status": "Task started successfully!", "data": job_id})
    else:
        return Response({"error": "Invalid request method."}, status=400)


@api_view(["POST", "GET"])
def post_on_social_media(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            job_id = data.get("job_id")
            post_1 = (
                os.path.join(
                    settings.MEDIA_ROOT, "generated_posts", f"post_1_{job_id}.pdf"
                ),
            )
            video_job = VideoProcessingJob.objects.get(job_id=job_id)
            caption_1 = get_caption(video_job.script)
            post_on_insta(post_1, caption_1)

            post_2 = (
                os.path.join(
                    settings.MEDIA_ROOT, "generated_posts", f"post_2_{job_id}.pdf"
                ),
            )
            caption_2 = get_caption(video_job.script)
            post_on_insta(post_2, caption_2)
            return Response({"status": "Posts created and posted successfully!"})
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)


def send_whatsapp_message_view(request):
    if request.method == "POST":
        send_whatsapp_message()
        return Response({"status": "Message sent successfully!"})
    else:
        return Response({"error": "Invalid request method."}, status=400)


def extract_thumbnail(video_path):
    """
    Extract thumbnail from MP4 file using OpenCV.
    Returns a base64 encoded string of the thumbnail image.
    """
    try:
        video = cv2.VideoCapture(video_path)

        success, frame = video.read()
        if not success:
            raise Exception("Could not read video file")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(frame_rgb)

        max_size = (800, 450)
        pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        video.release()

        return image_base64

    except Exception as e:
        raise Exception(f"Error extracting thumbnail: {str(e)}")


@api_view(["POST"])
def send_email_with_video(request):
    """
    Send emails with a video thumbnail linking to a YouTube video.
    Fetches the job ID from the request body and dynamically constructs the video path.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        # Parse the job_id from the request body
        body = json.loads(request.body)
        job_id = body.get("job_id")

        print(job_id)

        if not job_id:
            return JsonResponse(
                {"error": "Missing job_id in request body."}, status=400
            )

        # Construct the video path dynamically
        video_file_path = os.path.join(
            settings.MEDIA_ROOT, "generated_videos", f"{job_id}.mp4"
        )

        if not os.path.exists(video_file_path):
            return JsonResponse({"error": "Video file does not exist."}, status=404)

        csv_file_path = os.path.join(
            settings.MEDIA_ROOT, "target_audience", f"{job_id}.csv"
        )
        title = "Sample Video Title"
        description = "Description of the video."
        tags = ["sample", "video", "youtube"]
        category_id = "22"

        # Extract thumbnail from the video
        thumbnail_base64 = extract_thumbnail(video_file_path)

        # Upload video to YouTube
        video_id = upload_video_to_youtube(
            video_file_path, title, description, tags, category_id
        )

        # Construct YouTube video URL
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ad_text = "This is an ad text. Check out this video!"

        # Read email addresses from CSV and send emails
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row

            for row in islice(reader, 1):

                print(row)
                if len(row) < 2:
                    continue

                recipient_name = row[0].strip()
                recipient_email = row[18].strip()

                if not recipient_name or not recipient_email:
                    continue

                subject = "Check Out This Video"
                message = f"""
                    <html>
                    <body>
                        <p>Hi {recipient_name},</p>
                        <p>{ad_text}</p>
                        <p>Click the link below to watch the video:</p>
                        <p><a href="{video_url}"><img src="cid:thumbnail" alt="Watch Video" style="width: 60%; max-width: 600px;"/></a></p>
                    </body>
                    </html>
                """

                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                )
                email.content_subtype = "html"

                # Attach the thumbnail image
                image_data = base64.b64decode(thumbnail_base64)
                image = MIMEImage(image_data, _subtype="jpeg")
                image.add_header("Content-ID", "<thumbnail>")
                image.add_header(
                    "Content-Disposition", 'inline; filename="thumbnail.jpg"'
                )

                email.attach(image)
                email.send()

        return Response({"status": "Emails sent successfully!"})

    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)

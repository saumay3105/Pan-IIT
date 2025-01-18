from datetime import datetime
import os
import uuid
from django.db import models


def upload_to_unique_filename(instance, filename):
    # Get the file name and extension
    base_filename, extension = os.path.splitext(filename)

    # Get the current timestamp as a string
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Combine the original filename with the timestamp and the extension
    unique_filename = f"{base_filename}_{timestamp}{extension}"

    # Save the file in the 'uploaded_documents/' folder
    return os.path.join("uploaded_documents", unique_filename)


class VideoProcessingJob(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = models.FileField(upload_to=upload_to_unique_filename, null=True, blank=True)
    script = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("queued", "Queued"),
            ("processing", "Processing"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
    )
    video_preference = models.TextField()
    language = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": str(self.job_id),
            "job_id": str(self.job_id),
            "status": self.status,
        }


class Video(models.Model):
    video_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    video_job = models.ForeignKey(VideoProcessingJob, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField()
    thumbnail = models.ImageField(null=True, blank=True)
    visemes = models.JSONField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

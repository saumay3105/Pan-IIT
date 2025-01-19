import os
import uuid

from celery import shared_task

from core.utils.post_generator import TemplateContent, add_text_to_design_template
from core.utils.instagram_utils import generate_post_content
from video_generator.models import VideoProcessingJob
from django.conf import settings


@shared_task
def generate_image_posts(job_id: uuid.UUID, text: str = None):
    job = VideoProcessingJob.objects.get(job_id=job_id)
    if job.script:
        # posts_data = generate_post_content(job.script)
        posts_data = [
            {
                "heading": "Sentiment Analysis",
                "subtitle": "Public Opinion During the Pandemic",
                "button": "Learn More",
                "description": "public sentiment on social media evolved.",
                "address": "link-to-research-paper",
                "image_keyword": "social media sentiment analysis graph",
            },
            {
                "heading": "AI & Pandemic Response",
                "subtitle": "Transformer Models Outperform in Sentiment Analysis",
                "button": "Explore the Study",
                "description": "A study using 90,000 tweets shows that advanced AI models.",
                "address": "link-to-research-paper",
                "image_keyword": "AI graph showing BERT's superior performance",
            },
        ]
        if len(posts_data) >= 1:
            post_content_1 = TemplateContent(
                heading=posts_data[0].get("heading"),
                subtitle=posts_data[0].get("subtitle"),
                button=posts_data[0].get("button"),
                description=posts_data[0].get("description"),
                email=posts_data[0].get("address"),
                image_url="https://fdczvxmwwjwpwbeeqcth.supabase.co/storage/v1/object/public/images/f383cda8-0c5c-4579-9606-0df72fcb9aee/1085f340-bfeb-424e-a9d5-723d1f63d29b.png",
            )
            post_content_2 = TemplateContent(
                heading=posts_data[1].get("heading"),
                subtitle=posts_data[1].get("subtitle"),
                button=posts_data[1].get("button"),
                description=posts_data[1].get("description"),
                email=posts_data[1].get("address"),
                image_url="https://fdczvxmwwjwpwbeeqcth.supabase.co/storage/v1/object/public/images/f383cda8-0c5c-4579-9606-0df72fcb9aee/1085f340-bfeb-424e-a9d5-723d1f63d29b.png",
            )
            current_file_path = os.path.dirname(__file__)
            pdf_path_1 = os.path.join(current_file_path, "3.pdf")
            pdf_path_2 = os.path.join(current_file_path, "1.pdf")

            add_text_to_design_template(
                pdf_path_1,
                os.path.join(
                    settings.MEDIA_ROOT, "generated_posts", f"post_1_{job_id}.pdf"
                ),
                "3",
                post_content_1,
            )
            add_text_to_design_template(
                pdf_path_2,
                os.path.join(
                    settings.MEDIA_ROOT, "generated_posts", f"post_2_{job_id}.pdf"
                ),
                "2",
                post_content_2,
            )

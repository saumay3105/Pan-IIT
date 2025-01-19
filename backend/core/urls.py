from django.urls import path
from .views import (
    send_email_with_video,
    create_posts,
    post_on_social_media,
    send_whatsapp_message_view,
)

urlpatterns = [
    path("send-emails/", send_email_with_video, name="send_emails"),
    path("create-post/", create_posts, name="create_post"),
    path("post-on-social-media/", post_on_social_media, name="post_on_social_media"),
    path("send-whatsapp/", send_whatsapp_message_view, name="whatsapp_message"),
]

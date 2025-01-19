from django.urls import path
from .views import send_email_with_video, create_posts

urlpatterns = [
    path("send-emails/", send_email_with_video, name="send_emails"),
    path("create-post/", create_posts, name="create_post"),
]

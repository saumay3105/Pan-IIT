from django.urls import path
from .views import start_scraping, send_email_with_video

urlpatterns = [
    path("start-scraping/", start_scraping),
    path('send-emails/', send_email_with_video, name='send_emails'),
]

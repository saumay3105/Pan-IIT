from django.urls import path
from .views import start_scraping

urlpatterns = [
    path("start-scraping/", start_scraping),
    
]

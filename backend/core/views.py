from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils.scraping_utils import extract_page


@api_view(["POST", "GET"])
def start_scraping(request):
    if request.method == "POST":
        extract_page()
        print("called")

    return Response(data="scraped")

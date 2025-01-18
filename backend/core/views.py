from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from core.utils.scraping_utils import extract_page
from core.utils.text_processing import get_product_info

@api_view(["POST", "GET"])
def start_scraping(request):
    if request.method == "POST":
        extract_page()
        print("called")

    return Response(data="scraped")


@api_view(["POST"])
def text_extraction(request: HttpRequest):
    data = get_product_info()
    
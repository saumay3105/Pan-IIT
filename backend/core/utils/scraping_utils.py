import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .selenium_handler import get_driver


def scrape_trends(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    unique_trend_links = []
    trend_links = soup.find_all("a", class_="trend-link")

    # Extract and print the text of each link
    for link in trend_links:
        unique_trend_links.append(link.text)

    unique_trends = list(set(unique_trend_links))

    return unique_trends


def extract_page():
    browser = get_driver(headless=False)
    browser.get("https://trends24.in/india/")
    time.sleep(5)
    page_source = browser.page_source
    unique_trends = scrape_trends(page_source)
    browser.quit()
    return unique_trends

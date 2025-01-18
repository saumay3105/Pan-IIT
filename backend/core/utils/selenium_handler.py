from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(headless: bool = False):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")

    if headless:
        chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return browser

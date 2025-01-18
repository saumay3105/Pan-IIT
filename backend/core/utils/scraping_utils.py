import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .selenium_handler import get_driver


def search_product(browser, product_name, high_price):
    search_box = browser.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    current_url = browser.current_url
    filtered_url = f"{current_url}&s=exact-aware-popularity-rank&low-price=&high-price={high_price}"
    browser.get(filtered_url)


def extract_page(product_name: str, high_price: str):
    browser = get_driver(headless=False)
    browser.get("https://www.amazon.in")

    time.sleep(3)
    search_product(browser, product_name=product_name, high_price=high_price)
    browser.quit()

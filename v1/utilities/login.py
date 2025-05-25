import json
import time
import os
import undetected_chromedriver as uc
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

COOKIES_PATH = os.path.join(
    "cookies", "insta_cookies.json"
)  # path of cookies to be saved


def save_cookies(driver, path=COOKIES_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        json.dump(driver.get_cookies(), file)
    print("Cookies saved.")


def load_cookies(driver, path=COOKIES_PATH):
    with open(path, "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)  # putting cookies to the browsers memory
    return cookies


def login_to_instagram():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.get("https://www.instagram.com/")

    if os.path.exists(COOKIES_PATH):
        try:
            driver.delete_all_cookies()
            load_cookies(driver)
            driver.get("https://www.instagram.com/")
            print("Logged in with saved cookies.")
            return driver
        except Exception as e:
            print(f"Failed to load cookies. Error: {e}")

    print("Please log in manually in the browser window for the first time...")
    time.sleep(30)  # You must manually log in here

    save_cookies(driver)
    return driver


# mobile view hunts possible for content level data
def login_to_instagram_mobile():
    mobile_emulation = {
        "deviceMetrics": {"width": 1500, "height": 689, "pixelRatio": 2.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    }

    options = Options()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://www.instagram.com/")

    if os.path.exists(COOKIES_PATH):
        try:
            driver.delete_all_cookies()
            load_cookies(driver)
            driver.get("https://www.instagram.com/")
            print("Logged in with saved cookies.")
            return driver
        except Exception as e:
            print(f"Failed to load cookies. Error: {e}")

    print("Please log in manually in the browser window for the first time...")
    time.sleep(30)  # You must manually log in here

    save_cookies(driver)
    return driver

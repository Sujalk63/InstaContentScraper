from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
from utilities.load_done_status import load_done_status
from utilities.save_to_excel import save_data_to_excel
from hunting_data.modules.hunt_profile_data_functions import *
from hunting_data.modules.hunt_content_data_functions import *
from username_scraping.modules.scrape_usernames_from_explore import click_post
from urllib.parse import urlparse

t = 2

def huntContent(driver, username, data):

    content_data = build_content_template()

    try:

        # # post type
        # content_data["post_type"] = fetch_post_type(driver)
        # print(content_data["post_type"])

        # # content id
        # content_data["content_id"] = fetch_content_id(driver)
        # print(content_data["content_id"])

        # post time
        content_data["posted_time_details"] = fetch_posted_time(driver)
        print(content_data["posted_time_details"])
        day, hour, time_str = parse_posted_time_details(content_data["posted_time_details"])
        content_data["day_of_week"] = day
        content_data["hour_of_day"] = hour
        content_data["time_am_pm"] = time_str
        print(content_data["day_of_week"], content_data["hour_of_day"], content_data["time_am_pm"])







        if "content" not in data:
            data["content"] = []

        data["content"].append(content_data)

        return data

    except Exception as e:
        print(f"❌ Failed to extract content ID for {username}: {e}")


def article_existence(driver):
    article = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "article")
        )  # or another known container
    )
    return article


def fetch_post_type(driver):
    article = article_existence(driver)
    is_reel = False
    try:
        article.find_element(By.TAG_NAME, "video")
        is_reel = True
    except:
        pass
    post_type = "Reel" if is_reel else "Post"
    return post_type


def fetch_content_id(driver):
    current_url = driver.current_url
    path_parts = urlparse(current_url).path.strip("/").split("/")
    content_id = path_parts[1] if len(path_parts) >= 2 else ""

    return content_id

def fetch_posted_time(driver):
    article_existence(driver)
    try:
        time_element = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.TAG_NAME, "time"))
        )
        return time_element.get_attribute("datetime")
    except Exception as e:
        print(f"❌ Failed to fetch posted time: {e}")
        return None

def parse_posted_time_details(posted_time_iso):
    try:
        dt = datetime.strptime(posted_time_iso, "%Y-%m-%dT%H:%M:%S.000Z")

        day_of_week = dt.strftime("%A")         # 'Monday', 'Tuesday', etc.
        hour_of_day = dt.hour                   # 0 to 23
        time_am_pm = dt.strftime("%I:%M %p")    # '03:32 PM'

        return day_of_week, hour_of_day, time_am_pm
    except Exception as e:
        print(f"❌ Error parsing date: {e}")
        return None, None, None


def build_content_template():
    return {
        "post_type": None,  # "Post" or "Reel"
        "content_id": None,
        "posted_time_details": None,
        "day_of_week": None,
        "hour_of_day": None,
        "time_am_pm": None,
        "video_duration": None,
        "aspect_ratio": None,
        "thumbnail_present": False,
        "tumbnail_link": None,
        "caption_text": None,
        "caption_length": None,
        "hashtags_used": [],
        "hashtag_count": 0,
        "mentions_count": 0,
        "all_mentions": [],
        "link_in_caption": None,
        "audio_used": None,
        "is_trending_audio": False,
        "likes_count": None,
        "comments_count": None,
        "views_count": None,
        "saves": None,
        "shares": None,
    }

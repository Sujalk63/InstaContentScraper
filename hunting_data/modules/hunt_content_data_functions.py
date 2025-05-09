from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from utilities.load_done_status import load_done_status
from utilities.save_to_excel import save_data_to_excel
from hunting_data.modules.hunt_profile_data_functions import *
from hunting_data.modules.hunt_content_data_functions import *
from username_scraping.modules.scrape_usernames_from_explore import click_post
from urllib.parse import urlparse



def huntContent(driver, username, data):


    content_data = build_content_template()

    try:

        # post type 
        content_data["post_type"] = fetch_post_type(driver)
        print(content_data["post_type"])

        content_data["content_id"] = fetch_content_id(driver)
        print(content_data["content_id"])

        if "content" not in data:
            data["content"] = []
        
        data["content"].append(content_data)

        return data

    except Exception as e:
        print(f"❌ Failed to extract content ID for {username}: {e}")


def article_existence(driver):
    article = WebDriverWait(driver, 10).until(
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
    path_parts = urlparse(current_url).path.strip('/').split('/')
    content_id = path_parts[1] if len(path_parts) >= 2 else ""

    return content_id

def build_content_template():
    return {
        "post_type": None,  # "Post" or "Reel"
        "content_id": "",
        "posted_time": None,
        "day_of_week": "",
        "hour_of_day": "",
        "video_duration": None,
        "aspect_ratio": "",
        "thumbnail_present": False,
        "tumbnail_link": "",
        "caption_text": "",
        "caption_length": 0,
        "hashtags_used": [],
        "hashtag_count": 0,
        "mentions_count": 0,
        "all_mentions": [],
        "link_in_caption": "",
        "audio_used": "",
        "is_trending_audio": False,
        "likes_count": 0,
        "comments_count": 0,
        "views_count": None,
        "saves": None,
        "shares": None,
    }


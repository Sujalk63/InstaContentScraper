from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from utilities.load_done_status import load_done_status
from utilities.save_to_excel import save_data_to_excel
from hunting_data.modules.hunt_profile_data_functions import *
from hunting_data.modules.hunt_content_data_functions import *


def huntPost(driver, username, data):
    print("working")


def huntReel(driver, username, data):
    print("working")





def build_content_template(post_type):
    return {
        "content_id": "",
        "post_type": post_type,  # "Post" or "Reel"
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


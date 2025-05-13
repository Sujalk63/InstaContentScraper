from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from math import gcd
import html
from datetime import datetime
from utilities.load_done_status import load_done_status
from utilities.save_to_excel import save_data_to_excel
from hunting_data.modules.hunt_profile_data_functions import *
from hunting_data.modules.hunt_content_data_functions import *
from username_scraping.modules.scrape_usernames_from_explore import click_post
from urllib.parse import urlparse
import math

t = 1

def huntContent(driver, username, data):

    content_data = build_content_template()

    try:

        # # post type
        content_data["post_type"] = fetch_post_type(driver)
        # print(content_data["post_type"])

        # # content id
        # content_data["content_id"] = fetch_content_id(driver)
        # print(content_data["content_id"])

        # # post time
        # content_data["posted_time_details"] = fetch_posted_time(driver)
        # print(content_data["posted_time_details"])
        # day, hour, time_str = parse_posted_time_details(content_data["posted_time_details"])
        # content_data["day_of_week"] = day
        # content_data["hour_of_day"] = hour
        # content_data["time_am_pm"] = time_str
        # print(content_data["day_of_week"], content_data["hour_of_day"], content_data["time_am_pm"])

        # # video duration
        # content_data["video_duration"] = fetch_video_duration(driver)
        # print(content_data["video_duration"])

        # # aspect ratio
        # content_data["aspect_ratio"] = fetch_aspect_ratio(driver)
        # print(content_data["aspect_ratio"])

        # caption data
        caption_data = fetch_caption_text(driver)
        content_data["caption_text"] = caption_data["text"]
        content_data["caption_length"] = caption_data["character_count"]
        content_data["no_of_line_changes"] = caption_data["br_count"]

        caption_mentions_hastags = fetch_caption_mentions_hastags(content_data["caption_text"])
        content_data["hashtags_used"] = caption_mentions_hastags["hashtags_used"]
        content_data["hashtag_count"] = caption_mentions_hastags["hashtag_count"]
        content_data["all_mentions"] = caption_mentions_hastags["all_mentions"]
        content_data["mentions_count"] = caption_mentions_hastags["mentions_count"]

        # Audio 
        audio_info = fetch_audio_info(driver)
        content_data["audio_used"] = audio_info["audio_used"]
        content_data["is_trending_audio"] = audio_info["is_trending_audio"]

        print(content_data["audio_used"])
        print(content_data["is_trending_audio"])






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
    is_reel = False
    try:
        article = article_existence(driver)
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
    try:
        article_existence(driver)
        time_element = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.TAG_NAME, "time"))
        )
        return time_element.get_attribute("datetime")
    except Exception as e:
        print(f"❌ Failed to fetch posted time: {e}")
        return None


def fetch_video_duration(driver):
    try:
        article_existence(driver)
        video_element = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        # Use JavaScript to access the duration property of the video
        duration = driver.execute_script("return arguments[0].duration;", video_element)

        if duration and duration > 0:
            # Convert seconds to mm:ss format
            mins = int(duration // 60)
            secs = int(duration % 60)
            return f"{mins:02d}:{secs:02d}"
        else:
            return "00:00"
    except Exception as e:
        print("Error fetching video duration:", e)
        return None
    


def fetch_aspect_ratio(driver):
    try:
        article_existence(driver)
        # Try for video first
        video = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        width = driver.execute_script("return arguments[0].videoWidth;", video)
        height = driver.execute_script("return arguments[0].videoHeight;", video)

    except:
        try:
            # If video not found, try for image
            image = WebDriverWait(driver, t).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            width = driver.execute_script("return arguments[0].naturalWidth;", image)
            height = driver.execute_script("return arguments[0].naturalHeight;", image)
        except Exception as e:
            print(f"❌ Failed to fetch aspect ratio: {e}")
            return None

    try:
        if width and height:
            divisor = gcd(width, height)
            return f"{int(width / divisor)}:{int(height / divisor)}"
        else:
            return "Unknown"
    except:
        return None


def fetch_caption_text(driver): 
    try:
        article_existence(driver)

        h1_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, "//article//div//h1[@dir='auto']"))
        )

        raw_html = h1_elem.get_attribute("innerHTML")

        # Count <br> tags (each counts as 1 char)
        br_count = raw_html.count("<br>")

        # Replace <br> with a space for cleaner text output
        html_with_spaces = raw_html.replace("<br>", " ")

        # Unescape HTML (like &amp;)
        html_with_spaces = html.unescape(html_with_spaces)

        # Remove all tags but keep inner text of <a> and normal text
        text_only = re.sub(r'<[^>]+>', '', html_with_spaces)

        # Final clean text
        final_text = text_only.strip()

        # Total character count = visible text chars + <br> count
        total_characters = len(final_text) + br_count

        return {
            "text": final_text,
            "br_count": br_count,
            "character_count": total_characters
        }

    except Exception as e:
        print(f"❌ Failed to fetch caption: {e}")
        return {
            "text": None,
            "br_count": 0,
            "character_count": 0
        }


def fetch_caption_mentions_hastags(caption_text):
    try:
        # Extract hashtags (e.g., #parentingtips)
        hashtags = re.findall(r'#\w+', caption_text)
        
        # Extract mentions (e.g., @sujalK)
        mentions = re.findall(r'@\w+', caption_text)
        
        return {
            "hashtags_used": hashtags,
            "hashtag_count": len(hashtags),
            "all_mentions": mentions,
            "mentions_count": len(mentions)
        }
    except Exception as e:
        print(f"❌ Failed to extract hashtags and mentions: {e}")
        return {
            "hashtags_used": [],
            "hashtag_count": 0,
            "all_mentions": [],
            "mentions_count": 0
        }
    
def fetch_audio_info(driver):
    try:
        article_existence(driver)

        # Wait for audio section anchor
        audio_section = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, "//article//a[contains(@href, '/audio/')]"))
        )

        # Extract audio name (text inside span)
        try:
            audio_name_elem = audio_section.find_element(By.XPATH, ".//span")
            audio_used = audio_name_elem.text.strip()
        except:
            audio_used = None

        # Check for trending icon (usually has aria-label='Trending')
        try:
            trending_icon = audio_section.find_element(By.XPATH, ".//svg[@aria-label='Trending']")
            is_trending_audio = True
        except:
            is_trending_audio = False

        return {
            "audio_used": audio_used,
            "is_trending_audio": is_trending_audio
        }

    except Exception as e:
        print(f"❌ Failed to fetch audio info: {e}")
        return {
            "audio_used": None,
            "is_trending_audio": False
        }


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
        # "thumbnail_present": False,
        # "tumbnail_link": None,
        "caption_text": None,
        "caption_length": None,
        "no_of_line_changes": None,
        "hashtags_used": [],
        "hashtag_count": 0,
        "all_mentions": [],
        "mentions_count": 0,
        "audio_used": None,
        "is_trending_audio": False,
        "likes_count": None,
        "comments_count": None,
        "views_count": None,
        "saves": None,
        "shares": None,
    }


# https://scontent.cdninstagram.com/v/t51.71878-15/496360173_1393321048749845_8137806010030375186_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=111&ig_cache_key=MzYyOTQwNDYyNDU5NzYwMTM4MQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&_nc_ohc=RUB3m5s14zgQ7kNvwHuiCz4&_nc_oc=AdnWanqWlDpGmi9ZNVN8UZ3HXnOonym_aoDMrKLNP6MWADTtSNDER589piC9gbMqjIRwAayZBehbHQxzJHckiUvg&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.cdninstagram.com&_nc_gid=g2agS6wxIgDcPcrjRBWomw&oh=00_AfLASXHsCq1KYrBL5Dn8e6Z6i_G989rfz4DY0a-9sqoJeQ&oe=6827ACEF

# https://scontent.cdninstagram.com/v/t51.75761-15/485878527_17933183910007501_3479559491525146137_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&ig_cache_key=MzU5MzI3NjYzNTk1NDk1ODc0NDE3OTMzMTgzOTA0MDA3NTAx.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&_nc_ohc=wNwYxwpZkh8Q7kNvwF2iIkz&_nc_oc=AdlUYUUQ1mYakdDxHcuzZQbRBbUjKO3vl5KSoBQQLVLhfpcoC9irZpnpcOz6ytK75IX7bvYPtfrmYYnKSoZENQYG&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.cdninstagram.com&_nc_gid=Rp-n8mTZskL5neJvNoAaaw&oh=00_AfKVpZbF3_J27a4lYXFkEjd892OvuJuFVEA57dYAtYzoYA&oe=6827A83D

# https://scontent.cdninstagram.com/v/t51.75761-15/486288920_17933180487007501_5600046053478966604_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&ig_cache_key=MzU5MDM0OTMxODk3OTAxOTczODE3OTMzMTgwNDg0MDA3NTAx.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&_nc_ohc=-K0axrO-7_gQ7kNvwGo8OS9&_nc_oc=AdllkdPBssChKNk6y5_ladBtzAoUKYlq-mDjnk3x9t2U_KJFMecxiriQDRKpc92Ex4_I3WucJHRhsSedEJgzXs6Z&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.cdninstagram.com&_nc_gid=Rp-n8mTZskL5neJvNoAaaw&oh=00_AfIOfoW-ypsqQA4puScl2g0mXbsniFuMgOZAjcHfl8HCKg&oe=6827BC3C

# https://scontent.cdninstagram.com/v/t51.71878-15/485012378_1407619340648828_1675637164226427015_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=107&ig_cache_key=MzU5MTc3NDAyNDM5MTA4MTkxMg%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&_nc_ohc=j2MRc8b6B0sQ7kNvwEBQ4Pm&_nc_oc=Adm6dg50yDUSvQ2ACoP5WgVqBveZBExzWCoQiIgFZ7yVFsVUOoDIlfwmPZyZHUo3GFGDHZL1ON_FU4TwiGrwCpvY&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=scontent.cdninstagram.com&_nc_gid=Rp-n8mTZskL5neJvNoAaaw&oh=00_AfJzAFvNyH3TU4SZI1Az5uuFktFAv1N3Q1uJ_HnrAJAJ-Q&oe=6827BAC6
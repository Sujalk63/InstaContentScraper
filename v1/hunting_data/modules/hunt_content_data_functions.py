import html
import pytz
import time
import re
import base64
import json
from math import gcd
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from hunting_data.modules.hunt_profile_data_functions import *
from hunting_data.modules.hunt_content_data_functions import *
from selenium.webdriver.support import expected_conditions as EC

t = 2


def huntContent(driver, username, data):

    content_data = build_content_template()

    try:
        # content id
        content_data["content_id"] = fetch_content_id(driver)
        print(
            "🟢 Started scraping for content id:",
            content_data["content_id"],
            "of",
            username,
        )

        # # post type
        content_data["post_type"] = fetch_post_type(driver)
        # print("Post type:", content_data["post_type"])

        # post time
        content_data["posted_time_details"] = fetch_posted_time(driver)
        # print("Posted time details:", content_data["posted_time_details"])
        day, hour, time_str = parse_posted_time_details(
            content_data["posted_time_details"]
        )
        content_data["day_of_week"] = day
        content_data["hour_of_day"] = hour
        content_data["time_am_pm"] = time_str
        # print(
        #     "Day:",
        #     content_data["day_of_week"],
        #     "Hour:",
        #     content_data["hour_of_day"],
        #     "Time:",
        #     content_data["time_am_pm"],
        # )

        # video duration
        content_data["video_duration"] = fetch_video_duration(driver)
        # print("video duration", content_data["video_duration"])

        # aspect ratio
        content_data["aspect_ratio"] = fetch_aspect_ratio(driver)
        # print("Aspect ratio", content_data["aspect_ratio"])

        # caption data
        caption_data = fetch_caption_text(driver)
        content_data["caption_text"] = caption_data["text"]
        content_data["caption_length"] = caption_data["character_count"]
        content_data["no_of_line_changes"] = caption_data["br_count"]
        # print("Text:", content_data["caption_text"])
        # print("Length of caption:", content_data["caption_length"])
        # print("No of lines changes:", content_data["no_of_line_changes"])

        caption_mentions_hastags = fetch_caption_mentions_hastags(
            content_data["caption_text"]
        )
        content_data["hashtags_used"] = caption_mentions_hastags["hashtags_used"]
        content_data["hashtag_count"] = caption_mentions_hastags["hashtag_count"]
        content_data["all_mentions"] = caption_mentions_hastags["all_mentions"]
        content_data["mentions_count"] = caption_mentions_hastags["mentions_count"]
        # print("Hastags", content_data["hashtags_used"])
        # print("Hastag count", content_data["hashtag_count"])
        # print("All mentions", content_data["all_mentions"])
        # print("Mentions count", content_data["mentions_count"])

        # Audio
        header_info = fetch_top_header_info(driver)
        content_data["audio_used"] = header_info["audio_used"]
        content_data["post_context"] = header_info["post_context"]
        content_data["paid_partnership"] = header_info["paid_partnership"]
        # print("Audio used:", content_data["audio_used"])
        # print("Post context:", content_data["post_context"])
        # print("Partnership:", content_data["paid_partnership"])

        engagement_metrics = fetch_engagement_metrics(driver)
        content_data["likes_count"] = engagement_metrics["likes_count"]
        content_data["comments_count"] = engagement_metrics["comments_count"]
        # content_data["views_count"] = engagement_metrics["views_count"]
        # content_data["saves"] = engagement_metrics["saves"]
        # content_data["shares"] = engagement_metrics["shares"]

        # print("Like count:", content_data["likes_count"])
        # print("Comments count:", content_data["comments_count"])
        # print("Views count:",content_data["views_count"])
        # print("Saves count:",content_data["saves"])
        # print("Shares count:",content_data["shares"])

        if "content" not in data:
            data["content"] = []

        data["content"].append(content_data)

        print(
            "✅ Scrape complete for content id:",
            content_data["content_id"],
            "of",
            username,
        )

        return data

    except KeyboardInterrupt:
        print(f"⚠️ Interrupted while scraping a post for {username}")
        return data
        raise  # Re-raise to bubble it up to the outer try block

    except Exception as e:
        print(f"❌ Failed to content for {username}: {e}")


def article_existence(driver):
    article = WebDriverWait(driver, t).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "article")
        )  # or another known container
    )
    return article


def fetch_content_id_only(driver):
    try:
        content_id = fetch_content_id(driver)
        return content_id
    except Exception as e:
        print(f"❌ Failed to fetch content_id: {e}")
        return None


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
        return None


def fetch_aspect_ratio(driver):
    try:
        article_existence(driver)
        # Try for video first
        video = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        # print("found video:", video)
        width = driver.execute_script("return arguments[0].videoWidth;", video)
        height = driver.execute_script("return arguments[0].videoHeight;", video)

    except:
        try:
            # If video not found, try for image
            image = WebDriverWait(driver, t).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@role='button' and contains(@class, 'x1qjc9v5')]//img"
                        "[contains(@class, 'x5yr21d') and contains(@class, 'xu96u03') and contains(@class, 'x10l6tqk') and contains(@class, 'x13vifvy') and contains(@class, 'x87ps6o') and contains(@class, 'xh8yej3')]",
                    )
                )
            )
            # src = image.get_attribute("src")
            # print("found image:", src)
            width = driver.execute_script("return arguments[0].naturalWidth;", image)
            height = driver.execute_script("return arguments[0].naturalHeight;", image)
        except Exception as e:
            print(f"❌ Failed to fetch aspect ratio: {e}")
            return None

    try:
        if width and height:
            return closest_common_aspect_ratio(width, height)
        # else:
        #     return "Unknown"
    except:
        print(f"❌ Error calculating aspect ratio: {e}")
        return None


def closest_common_aspect_ratio(width, height):
    # Common aspect ratios to check against (width:height)
    common_ratios = {
        "1:1": (1, 1),
        "4:5": (4, 5),
        "5:4": (5, 4),
        "9:16": (9, 16),
        "16:9": (16, 9),
        "3:4": (3, 4),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "3:2": (3, 2),
    }

    # Calculate actual ratio as float
    actual_ratio = width / height

    # Find closest common ratio by minimal absolute difference
    closest_label = None
    smallest_diff = float("inf")
    for label, (w, h) in common_ratios.items():
        ratio = w / h
        diff = abs(actual_ratio - ratio)
        if diff < smallest_diff:
            smallest_diff = diff
            closest_label = label

    # Accept only if difference is small enough (tweak threshold if needed)
    if smallest_diff < 0.05:
        return closest_label
    else:
        # Return simplified raw ratio if no close match found
        divisor = gcd(width, height)
        return f"{int(width / divisor)}:{int(height / divisor)}"


def fetch_caption_text(driver):
    try:
        article_existence(driver)

        try:
            more_button = WebDriverWait(driver, t).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button' and .//span[text()='more']]")
                )
            )
            # print("printing more button:", more_button)
            # more_button.click()
            driver.execute_script(
                "arguments[0].click();", more_button
            )  # Using JavaScript click to bypass Selenium click issues (e.g., element hidden, overlapped, or not interactable)
            # print("clicked more button")
            # time.sleep(1)  # brief wait after clicking
        except:
            print("didint find more button")
            pass  # no "more" button, proceed as usual

        h1_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located(
                (By.XPATH, "//article//div//h1[@dir='auto']")
            )
        )

        raw_html = h1_elem.get_attribute("innerHTML")

        # Count <br> tags (each counts as 1 char)
        br_count = raw_html.count("<br>")

        # Replace <br> with a space for cleaner text output
        html_with_spaces = raw_html.replace("<br>", " ")

        # Unescape HTML (like &amp;)
        html_with_spaces = html.unescape(html_with_spaces)

        # Remove all tags but keep inner text of <a> and normal text
        text_only = re.sub(r"<[^>]+>", "", html_with_spaces)

        # Final clean text
        final_text = text_only.strip()

        # Total character count = visible text chars + <br> count
        total_characters = len(final_text) + br_count

        return {
            "text": final_text,
            "br_count": br_count,
            "character_count": total_characters,
        }

    except Exception as e:
        print(f"❌ Failed to fetch caption: {e}")
        return {"text": None, "br_count": 0, "character_count": 0}


def fetch_caption_mentions_hastags(caption_text):
    try:
        # Extract hashtags (e.g., #parentingtips)
        hashtags = re.findall(r"#\w+", caption_text)

        # Extract mentions (e.g., @sujalK)
        mentions = re.findall(r"@\w+", caption_text)

        return {
            "hashtags_used": hashtags,
            "hashtag_count": len(hashtags),
            "all_mentions": mentions,
            "mentions_count": len(mentions),
        }
    except Exception as e:
        print(f"❌ Failed to extract hashtags and mentions: {e}")
        return {
            "hashtags_used": [],
            "hashtag_count": 0,
            "all_mentions": [],
            "mentions_count": 0,
        }


def fetch_top_header_info(driver):
    try:
        article_existence(driver)

        header_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, "//article//header"))
        )

        # Start defaults
        post_context = None
        paid_partnership = None
        audio_used = None

        # --- 1. Audio Info ---
        try:
            # Audio is often at the bottom or near play bar
            audio_elem = WebDriverWait(driver, t).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div//a[contains(@href, '/reels/audio/')]")
                )
            )
            audio_text = audio_elem.text.strip()

            if "original audio" in audio_text.lower():
                audio_used = "original"
            elif audio_text:
                audio_used = audio_text
        except:
            audio_used = None

        # --- 2. Location (top header clickable link) ---
        try:
            post_context = header_elem.find_element(By.XPATH, ".//div[@dir='auto']//a")
            post_context = post_context.text.strip()
        except:
            post_context = None

        # --- 3. Paid Partnership (usually a span element with text like "Paid partnership with") ---
        try:
            partnership_elem = header_elem.find_element(
                By.XPATH, ".//span[contains(text(), 'Paid partnership')]"
            )
            paid_partnership = partnership_elem.text.strip()
        except:
            paid_partnership = None

        return {
            "audio_used": audio_used,
            "post_context": post_context,
            "paid_partnership": paid_partnership,
        }

    except Exception as e:
        print(f"❌ Failed to fetch top header info: {e}")
        return {"audio_used": None, "post_context": None, "paid_partnership": None}


def fetch_engagement_metrics(driver):
    try:
        article_existence(driver)

        # --- Likes Count ---
        likes = None
        try:
            like_elem = driver.find_element(
                By.XPATH, "//article//section//span[contains(@class, 'html-span')]"
            )
            like_text = like_elem.text.strip()
            if re.search(r"\d", like_text):
                likes = convert_to_number(re.findall(r"\d[\d.,KMB]*", like_text)[0])
        except:
            likes = None

        # --- comments Count ---
        comments = None
        try:
            # comment_elem = driver.find_element(
            #     By.XPATH, "//a[contains(@href, '/comments/')]/span/span"
            # )
            # comment_text = comment_elem.text.strip()
            # print("text of comment:", comment_text)
            # if re.search(r"\d", comment_text):
            #     comments = convert_to_number(re.findall(r"\d[\d.,KMB]*", comment_text)[0])
            comment_link_elem = driver.find_element(
                By.XPATH, "//a[contains(@href, '/comments/')]"
            )

            # Try to find inner <span> if it exists (for multiple comments like: "View all 33 comments")
            try:
                inner_span = comment_link_elem.find_element(By.XPATH, ".//span/span")
                comment_text = inner_span.text.strip()
            except:
                # Fallback: Only one comment, use outer <span>
                outer_span = comment_link_elem.find_element(By.XPATH, ".//span")
                comment_text = outer_span.text.strip()

            # print(f"Extracted comment text: {comment_text}")

            # Extract number from text like "View 1 comment", "View all 33 comments"
            match = re.search(r"\d[\d.,KMB]*", comment_text)
            if match:
                comments = convert_to_number(match.group())
        except:
            comments = None

        return {
            "likes_count": likes,
            "comments_count": comments,
            # "views_count": None,
            # "saves": None,
            # "shares": None,
        }

    except Exception as e:
        print(f"❌ Failed to fetch engagement metrics: {e}")
        return {
            "likes_count": None,
            "comments_count": None,
            # "views_count": None,
            # "saves": None,
            # "shares": None,
        }


def parse_posted_time_details(posted_time_iso):
    try:
        # Step 1: Parse original ISO timestamp in UTC
        utc_time = datetime.strptime(posted_time_iso, "%Y-%m-%dT%H:%M:%S.000Z")
        utc_time = utc_time.replace(tzinfo=pytz.UTC)

        # Step 2: Convert to IST
        ist = pytz.timezone("Asia/Kolkata")
        ist_time = utc_time.astimezone(ist)

        day_of_week = ist_time.strftime("%A")
        hour_of_day = ist_time.hour
        time_am_pm = ist_time.strftime("%I:%M %p")

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
        "location": None,
        "paid_partnership": None,
        "likes_count": None,
        "comments_count": None,
        # "views_count": None,
        # "saves": None,
        # "shares": None,
    }


# https://scontent.cdninstagram.com/v/t51.75761-15/497106940_18014250902709093_1799818465998331702_n.jpg?stp=dst-jpegr_e35_tt6&_nc_cat=111&cb=30a688f7-097e4a6c&ccb=7-5&_nc_sid=58cdad&_nc_ohc=Jnac8d5pfo8Q7kNvwFlAEF0&_nc_oc=AdlxmQXtN7whpm9_k3GvqDm_lg5fTjJyJdWm7Hqcd2h7ZKxzRlGT0y1aaEaDJM_dhMuP9JStNYUVD7JEnOdzmQMe&_nc_ad=z-m&_nc_cid=1174&_nc_zt=23&se=-1&_nc_ht=scontent.cdninstagram.com&_nc_gid=Q15RtQrdh5pOkEE1DBLy_g&oh=00_AfJfKSjRnHZeCHPvh8zI2huiBPgkZCbfim9TXRIxNBySVw&oe=682E0A8F

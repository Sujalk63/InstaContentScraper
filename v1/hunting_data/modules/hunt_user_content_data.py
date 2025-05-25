import time
import pandas as pd
from selenium.webdriver.common.by import By
from utilities.save_to_excel import save_data_to_excel
from selenium.webdriver.support.ui import WebDriverWait
from utilities.load_scaped_data import *
from hunting_data.modules.hunt_content_data_functions import *
from hunting_data.modules.hunt_profile_data_functions import *
from selenium.webdriver.support import expected_conditions as EC
from username_scraping.modules.scrape_usernames_from_explore import next_button_click
from username_scraping.modules.scrape_usernames_from_explore import click_post
from utilities.flatten_data import flatten_data_for_saving


def scrape_content(driver, usernames=None):

    # Handle all three input cases
    if usernames is None:
        df = pd.read_excel("usernames.xlsx")  # later usernames
        usernames_list = df["Username"].dropna().unique().tolist()
    elif isinstance(usernames, str):
        usernames_list = [usernames.strip()]
    elif isinstance(usernames, list):
        usernames_list = [u.strip() for u in usernames if isinstance(u, str)]
    else:
        print("❌ Invalid input format for usernames.")
        return

    print(f"🔍 Total usernames to scrape content for: {len(usernames_list)}")

    # Load scraping status to avoid re-scraping
    done_usernames = load_done_status(
        excel_path="usernames.xlsx", coloumn="is_content_data_fetched"
    )  # later usernames
    content_data_batch = []

    try:
        for i, username in enumerate(usernames_list):
            print(f"{username} {i}")
            if username in done_usernames:
                print(f"⏭️ Skipping {username} (already marked as Done)")
                continue

            data, interurupted = fetch_content_data(driver, username)

            if data is None:
                print(f"⚠️ {username} changed or deleted")
                mark_profile_done(username)
                continue

            flattened_posts = flatten_data_for_saving(data)
            content_data_batch.extend(flattened_posts)

            if not interurupted:
                if content_data_batch:
                    print(
                        f"💾 Whole data fetched for {username}, saving and marking as done"
                    )
                    save_data_to_excel(
                        content_data_batch,
                        file_path="usernames_content_data.xlsx",
                        table_name="contentDataTable",
                    )
                for profile in content_data_batch:
                    mark_profile_done(profile["Username"])
                # print("Username Marked done")
            else:
                if content_data_batch:
                    print(
                        f"⚠️  💾Partial data fetched for {username}, saving and not marking as done."
                    )
                    save_data_to_excel(
                        content_data_batch,
                        file_path="usernames_content_data.xlsx",
                        table_name="contentDataTable",
                    )

    except KeyboardInterrupt:
        if content_data_batch:
            print(
                f"⚠️ Saving partial content data of length {len(content_data_batch)} for {username}"
            )
            save_data_to_excel(
                content_data_batch,
                file_path="usernames_content_data.xlsx",
                table_name="contentDataTable",
            )


def fetch_content_data(driver, username):

    t = 2

    done_content_ids = load_scraped_content_ids(
        excel_path="usernames_content_data.xlsx"
    )
    url = f"https://www.instagram.com/{username}/"

    try:
        driver.get(url)
        WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.CLASS_NAME, "xrvj5dj"))
        )
    except Exception as e:
        print(f"❌ Profile page did not load properly for {username}: {e}")
        return None, False

    data = {
        "Username": username,
        "content": [],
    }

    click_post(driver)

    try:
        # n = 1
        while True:  # n<=5
            # n = n+1
            prev_url = driver.current_url

            # Fetch content_id only first
            content_id = fetch_content_id_only(driver)

            if content_id is None:
                print("❌ Could not get content_id, skipping this post...")
                try:
                    next_button_click(driver)
                    time.sleep(0.1)
                    new_url = driver.current_url
                    if prev_url == new_url:
                        print("❌ Reached last post, cannot move forward.")
                        break
                    continue
                except Exception:
                    print("❌ No more posts or failed to click next.")
                    break

            if content_id in done_content_ids:
                print(f"⏭️ Skipping already scraped content_id: {content_id}")
                try:
                    next_button_click(driver)
                    continue
                except Exception:
                    print("❌ No more posts or failed to click next.")
                    break

            data = huntContent(driver, username, data)
            done_content_ids.add(content_id)

            try:
                next_button_click(driver)
                time.sleep(0.1)
                new_url = driver.current_url
                if prev_url == new_url:
                    print("❌ Reached last post, cannot move forward.")
                    break
            except Exception:
                print("❌ No more posts or failed to click next.")
                break

    except KeyboardInterrupt:
        print(f"⚠️ Interrupted while scraping {username}, returning partial data...")
        return data, True  # Interrupted = True

    print(
        f"✅ Scraped data complete for: {username}, 🔢 total size of posts: {len(data['content'])}"
    )

    return data, False  # Interrupted = False means full scrape


def mark_profile_done(username, excel_path="usernames.xlsx"):  # later usernames
    mark_done(username, "is_content_data_fetched", excel_path)


# def fetch_content_data(driver, username):

#     t = 2

#     done_content_ids = load_scraped_content_ids(
#         excel_path="usernames_content_data.xlsx"
#     )
#     url = f"https://www.instagram.com/{username}/"

#     try:
#         driver.get(url)
#         WebDriverWait(driver, t).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "xrvj5dj"))
#         )
#     except Exception as e:
#         print(f"❌ Profile page did not load properly for {username}: {e}")
#         return None, False

#     data = {
#         "Username": username,
#         "content": [],
#     }

#     click_post(driver)

#     try:
#         while True:
#             prev_url = driver.current_url

#             content_id = fetch_content_id_only(driver)

#             if content_id is None:
#                 print("❌ Could not get content_id, skipping this post...")
#                 # Retry clicking next button
#                 retries = 3
#                 for attempt in range(retries):
#                     try:
#                         next_button_click(driver)
#                         # time.sleep(2)
#                         new_url = driver.current_url
#                         if new_url != prev_url:
#                             break
#                         else:
#                             print(
#                                 f"🔄 Retry {attempt+1}/{retries} – next button didn't work yet..."
#                             )
#                             # time.sleep(2.5)
#                     except Exception as e:
#                         print(
#                             f"⚠️ Next button not found (attempt {attempt+1}/{retries}): {e}"
#                         )
#                         # time.sleep(2)
#                 else:
#                     print(
#                         "❌ Reached last post or next button not available after retries."
#                     )
#                     break
#                 continue

#             if content_id in done_content_ids:
#                 print(f"⏭️ Skipping already scraped content_id: {content_id}")
#                 # Retry clicking next button
#                 retries = 3
#                 for attempt in range(retries):
#                     try:
#                         next_button_click(driver)
#                         # time.sleep(2)
#                         new_url = driver.current_url
#                         if new_url != prev_url:
#                             break
#                         else:
#                             print(
#                                 f"🔄 Retry {attempt+1}/{retries} – next button didn't work yet..."
#                             )
#                             # time.sleep(2.5)
#                     except Exception as e:
#                         print(
#                             f"⚠️ Next button not found (attempt {attempt+1}/{retries}): {e}"
#                         )
#                         # time.sleep(2)
#                 else:
#                     print(
#                         "❌ Reached last post or next button not available after retries."
#                     )
#                     break
#                 continue

#             data = huntContent(driver, username, data)
#             done_content_ids.add(content_id)

#             # Retry clicking next button
#             retries = 3
#             for attempt in range(retries):
#                 try:
#                     next_button_click(driver)
#                     # time.sleep(2)
#                     new_url = driver.current_url
#                     if new_url != prev_url:
#                         break
#                     else:
#                         print(
#                             f"🔄 Retry {attempt+1}/{retries} – next button didn't work yet..."
#                         )
#                         # time.sleep(2.5)
#                 except Exception as e:
#                     print(
#                         f"⚠️ Next button not found (attempt {attempt+1}/{retries}): {e}"
#                     )
#                     # time.sleep(2)
#             else:
#                 print(
#                     "❌ Reached last post or next button not available after retries."
#                 )
#                 break

#     except KeyboardInterrupt:
#         print(f"⚠️ Interrupted while scraping {username}, returning partial data...")
#         return data, True  # Interrupted = True

#     print(
#         f"✅ Scraped data complete for: {username}, 🔢 total size of posts: {len(data['content'])}"
#     )

#     return data, False  # Interrupted = False means full scrape


# def mark_profile_done(username, excel_path="usernames.xlsx"):  # later usernames
#     mark_done(username, "is_content_data_fetched", excel_path)

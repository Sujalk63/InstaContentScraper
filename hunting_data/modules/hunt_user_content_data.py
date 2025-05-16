import time
import pandas as pd
from selenium.webdriver.common.by import By
from utilities.save_to_excel import save_data_to_excel
from selenium.webdriver.support.ui import WebDriverWait
from utilities.load_done_status import load_done_status
from hunting_data.modules.hunt_content_data_functions import *
from hunting_data.modules.hunt_profile_data_functions import *
from selenium.webdriver.support import expected_conditions as EC
from username_scraping.modules.scrape_usernames_from_explore import next_button_click
from username_scraping.modules.scrape_usernames_from_explore import click_post


def scrape_content(driver, usernames=None, batch_size=100):

    # Handle all three input cases
    if usernames is None:
        df = pd.read_excel("usernames_dummy.xlsx")  # later usernames
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
        excel_path="usernames_dummy.xlsx", coloumn="is_content_data_fetched"
    )  # later usernames
    content_data_batch = []

    try:
        for i, username in enumerate(usernames_list):
            print(f"{username} {i}")
            if username in done_usernames:
                print(f"⏭️ Skipping {username} (already marked as Done)")
                continue

            data = fetch_content_data(driver, username)

            if data is None:
                print(f"⚠️ {username} changed or deleted")
                # mark_profile_done(username)
                continue

            content_data_batch.append(data)

            if len(content_data_batch) >= batch_size:
                save_data_to_excel(
                    content_data_batch,
                    file_path="usernames_content_data.xlsx",
                    table_name="contentDataTable",
                )

                print(f"✅ Saved batch of {batch_size} profiles to Excel.")
                for profile in content_data_batch:
                    mark_profile_done(profile["Username"])
                content_data_batch = []

    finally:
        if content_data_batch:
            print(
                f"⚠️ Saving final unsaved batch of {len(content_data_batch)} profiles."
            )
            save_data_to_excel(
                content_data_batch,
                file_path="usernames_content_data.xlsx",
                table_name="contentDataTable",
            )

            for profile in content_data_batch:
                mark_profile_done(profile["Username"])


def fetch_content_data(driver, username):

    url = f"https://www.instagram.com/{username}/"

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "xrvj5dj"))
        )
    except Exception as e:
        print(f"❌ Profile page did not load properly for {username}: {e}")
        return None

    data = {
        "username": username,
        "content": [],
    }

    click_post(driver)

    n = 1

    while n <= 13:
        n = n + 1
        prev_url = driver.current_url
        # Extract the content data for the current post
        huntContent(driver, username, data)

        # Try to click the next button
        try:
            time.sleep(2)
            next_button_click(driver)
            WebDriverWait(driver, 10).until(EC.url_changes(prev_url))
        except Exception as e:
            print(f"❌ No more posts or failed to click next: {e}")
            break

    print(data["content"])
    return data


def mark_profile_done(username, excel_path="usernames_dummy.xlsx"):  # later usernames
    mark_done(username, "is_content_data_fetched", excel_path)

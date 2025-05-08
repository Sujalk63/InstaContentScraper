from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from utilities.load_done_status import load_done_status
from utilities.save_to_excel import save_data_to_excel
from hunting_data.modules.hunt_profile_data_functions import *


def scrape_content(driver, usernames=None, batch_size=100):
    # Handle all three input cases
    if usernames is None:
        df = pd.read_excel("dummy_usernames.xlsx")  # later usernames
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
    done_usernames = load_done_status(excel_path="usernames_dummy.xlsx", coloumn="is_content_data_fetched") # later usernames
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
                mark_profile_done(username)
                continue

            content_data_batch.append(data)

            if len(content_data_batch) >= batch_size:
                save_data_to_excel(content_data_batch, file_path="usernames_content_data.xlsx", table_name="profileDataTable")

                print(f"✅ Saved batch of {batch_size} profiles to Excel.")
                for profile in content_data_batch:
                    mark_profile_done(profile["Username"])
                content_data_batch = []

    finally:
        if content_data_batch:
            print(f"⚠️ Saving final unsaved batch of {len(content_data_batch)} profiles.")
            save_data_to_excel(content_data_batch, file_path="usernames_content_data.xlsx", table_name="profileDataTable")

            for profile in content_data_batch:
                mark_profile_done(profile["Username"])

    


def fetch_content_data(driver, username):
    # print("working from fetch")
    url = f"https://www.instagram.com/{username}/"
            




def mark_profile_done(username, excel_path="usernames_dummy.xlsx"): # later usernames
    mark_done(username, "is_content_data_fetched", excel_path)


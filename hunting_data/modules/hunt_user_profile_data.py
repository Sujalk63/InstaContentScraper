import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # Importing pandas for saving to Excel

def scrape_profiles(driver, usernames=None):


    """
    Scrapes Instagram profile data.
    If `usernames` is None, reads from usernames.xlsx.
    If `usernames` is a string, treats it as a single username.
    If `usernames` is a list, scrapes all usernames in the list.
    """
    if usernames is None:
        # Batch mode from Excel
        df = pd.read_excel("usernames_dummy.xlsx")
        usernames_list = df["Username"].dropna().unique().tolist()
    elif isinstance(usernames, str):
        # Single username mode
        usernames_list = [usernames.strip()]
    elif isinstance(usernames, list):
        usernames_list = [u.strip() for u in usernames if isinstance(u, str)]
    else:
        print("Invalid input format for usernames.")
        return

    for username in usernames_list:
        data = fetch_profile_data(driver, username)
        # time.sleep(60)
        


def fetch_profile_data(driver, username):
    url = f"https://www.instagram.com/{username}/"

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'xrvj5dj'))
        )
    except Exception as e:
        print(f"Profile page did not load properly for {username}: {e}")
        return None

    driver.get(url)
    time.sleep(3)  # Allow page to load, will be replaced with WebDriverWait

    data = {
        "Username": username,
        "Full Name": None,
        "Number of Posts": None,
        "Followers Count": None,
        "Following Count": None,
        "Profile Bio": None,
        "External Link": None,
        "Email in Bio": None,
        "Collab/Mgmt Info": None,
        "Business Category Label": None,
        "Profile Picture URL": None,
        "Is Verified": False,
        "Professional Label": None
    }

    try:
        
        full_name = get_full_name(driver)
        print(f"{username}: {full_name}")

    except Exception as e:
        print(f"Error fetching {username}: {e}")

    return data

def get_full_name(driver):
    """
    Extracts the full name from an Instagram profile page.
    Assumes driver is already on the user's profile.
    Returns the full name or None if not found.
    """
    try:
        full_name_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "x1lliihq")]'))
        )
        return full_name_elem.text.strip() if full_name_elem.text else None
    except Exception:
        return None
    
    x1lliihq 
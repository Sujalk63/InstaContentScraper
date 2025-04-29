import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.navigate_to_reels import navigate_to_reels
from utilities.scroll_reel import scroll_reel
import pandas as pd  # Importing pandas for saving to Excel

# Function to scrape usernames from reels
def scrape_usernames_from_reels(driver):
    usernames = []
    
    try:
        # Navigate to Reels page
        navigate_to_reels(driver)

        while True:
            username = fetch_username(driver)
            if username:
                if username not in usernames:
                    usernames.append(username)
                    print(f"Fetched username: {username}")
                    
                    # Save immediately after each new username
                    save_usernames_to_excel(usernames)
                else:
                    print(f"Username '{username}' already scraped. Skipping.")
            else:
                print("Could not fetch username.")
            
            scroll_reel(driver)
            time.sleep(10)  # Wait for the next reel to load
            
    except KeyboardInterrupt:
        print("Stopped by user manually!")
         
    except Exception as e:
        print(f"{e}")


def fetch_username(driver):
    try:
        videos = driver.find_elements(By.TAG_NAME, 'video')
        
        for video in videos:
            is_playing = driver.execute_script("return arguments[0].paused === false;", video)
            if is_playing:
                print("Found currently playing reel.")
                
                # Traverse up the DOM to find the parent <a> tag with username
                parent = video.find_element(By.XPATH, "./ancestor::div[contains(@class, 'x1lliihq')]")
                a_tag = parent.find_element(By.XPATH, ".//a[contains(@href, '/reels/') and contains(@aria-label, ' reels')]")
                
                aria_label = a_tag.get_attribute("aria-label")
                print(f"Found aria-label: {aria_label}")
                
                if aria_label and " " in aria_label:
                    username = aria_label.split(" ")[0].strip()
                    print(f"Extracted username: {username}")
                    return username
                else:
                    print("aria-label does not contain expected format.")
                    return None

        print("No playing video found.")
        return None

    except Exception as e:
        print(f"Failed to fetch username: {e}")
        return None



def save_usernames_to_excel(usernames):
    if usernames:
        df_new = pd.DataFrame(usernames, columns=['Username'])
    
        if os.path.exists('usernames.xlsx'):
            df_existing = pd.read_excel('usernames.xlsx')
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.drop_duplicates(subset='Username', inplace=True)  # Optional: Remove duplicates
            df_combined.to_excel('usernames.xlsx', index=False)
        else:
            df_new.to_excel('usernames.xlsx', index=False)
        
        print("Updated 'usernames.xlsx' with new usernames!")
        

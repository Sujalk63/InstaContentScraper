# save cookies style
from dotenv import load_dotenv
from utilities.login import login_to_instagram
from hunting_data.hunt_user_data import hunt_user_data
from username_scraping.scrape_usernames import scrape_username

load_dotenv()

# Get logged-in driver (with cookies or manual login if first time)
driver = login_to_instagram()


try:
    driver.get("https://www.instagram.com/")
    driver.maximize_window()

    print("\nWhat would you like to do?")
    print("1. Scrape Usernames")
    print("2. Hunt User Data (Profile + Content)")

    task_choice = input("Enter your choice (1 or 2): ").strip()

    if task_choice == "1":
        scrape_username(driver)
    elif task_choice == "2":
        # You’ll define this next,
        hunt_user_data(driver)
    else:
        print("Invalid choice. Please enter 1 or 2.")

finally:
    input("Press Enter to close the browser...")
    driver.quit()


# ⏭️ Skipping archiiiii.x (already marked as Done)

# without using cookie

# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from dotenv import load_dotenv
# from utilities import navigate_to_explore




# # Import our modules
# from utilities.login import login_to_instagram
# from username_scraping.modules.scrape_usernames_from_explore import scrape_usernames_from_explore
# from username_scraping.modules.scrape_usernames_from_reels import scrape_usernames_from_reels

# # Load environment variables
# load_dotenv()

# # Setup Chrome Driver
# driver_path = r'driver/chromedriver.exe'
# service = Service(driver_path)
# driver = webdriver.Chrome(service=service)

# try:
#     driver.maximize_window()

#     # Login to Instagram
#     login_to_instagram(driver)

#     # Choose task phase
#     scrape_usernames_from_explore(driver)  # Scraping usernames via explore page
#     # scrape_usernames_from_reels(driver)      # Scraping usernames via reel section


# finally:
#     input("Press Enter to close the browser...")  # Give the user time to inspect the browser
#     driver.quit()  # Ensure the driver quits even if there was an error


# G7v$kR2#tLp9!XeQ

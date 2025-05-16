import time
import re
import os
import pandas as pd  # Importing pandas for saving to Excel
from selenium.webdriver.common.by import By
from utilities.login import login_to_instagram_mobile
from selenium.webdriver.support.ui import WebDriverWait
from hunting_data.modules.hunt_user_profile_data import *
from hunting_data.modules.hunt_user_content_data import *
from selenium.webdriver.support import expected_conditions as EC


def hunt_user_data(driver):
    print("\nChoose an option to hunt user data:")
    print("1. Hunt Profile level Data")
    print("2. Hunt Content level Data")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        print("\nHunting user profile level data...\n")
        scrape_profiles(driver)
    elif choice == "2":
        driver.quit()
        mobile_driver = login_to_instagram_mobile()
        mobile_driver.maximize_window()
        print("\nHunting user content level data...\n")
        scrape_content(mobile_driver)
    else:
        print("Invalid choice. Please enter 1 or 2.")


        

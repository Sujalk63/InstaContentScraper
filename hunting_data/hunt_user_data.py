import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # Importing pandas for saving to Excel
from hunting_data.modules.hunt_user_profile_data import *
from hunting_data.modules.hunt_user_content_data import *


def hunt_user_data(driver):
    print("\nChoose an option to hunt user data:")
    print("1. Hunt Profile level Data")
    print("2. Hunt Content level Data")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        print("\nHunting user profile level data...\n")
        scrape_profiles(driver)
    elif choice == "2":
        print("\nHunting user content level data...\n")
        scrape_content(driver)
    else:
        print("Invalid choice. Please enter 1 or 2.")

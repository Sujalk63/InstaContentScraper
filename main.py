import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Import our modules
from modules.login import login_to_instagram
from modules.navigate_to_reels import navigate_to_reels

# Load environment variables
load_dotenv()

# Setup Chrome Driver
driver_path = r'driver/chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

driver.maximize_window()

# Perform actions
login_to_instagram(driver)
navigate_to_reels(driver)

input("Press Enter to close the browser...")
driver.quit()

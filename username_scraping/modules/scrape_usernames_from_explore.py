import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.navigate_to_explore import navigate_to_explore
import pandas as pd  # Importing pandas for saving to Excel

# Function to scrape usernames from explore
def scrape_usernames_from_explore(driver):
    # usernames = []
    
    try:
        # Navigate to Explore page
        navigate_to_explore(driver)
        
        # Wait for the div containing the posts to be present
        clickable_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_aagw"))
        )
        
        click_post(driver, clickable_div)

        # Wait for the div containing the posts to be present
        next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='_abl-']"))
        )
        
        count = 100
         
        for c in range(count):
            time.sleep(3)
            next_button_click(next_button)
            print(f"✅ Clicked the 'Next' button. ({c+1})")

                
    except Exception as e:
        print(f"❌ {e}")

    # return usernames


def click_post(driver, clickable_div):
    driver.execute_script("arguments[0].scrollIntoView(true);", clickable_div)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", clickable_div)
    print("✅ Clicked on the post (div with class _aagw)")
        
        
def next_button_click(next_button):
        next_button.click()

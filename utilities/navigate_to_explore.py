import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from modules.scrape_usernames import scrape_usernames

def navigate_to_explore(driver):
    driver.get('https://www.instagram.com/explore/')
    
    # Wait until the explore grid loads
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'v1Nh3')]"))
        )
        print("✅ Successfully navigated to Explore page.")        
        
    except Exception as e:
        print(f"❌ Failed to load Explore page: {e}")

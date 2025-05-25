import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from modules.scrape_usernames import scrape_usernames

def navigate_to_explore(driver):
    driver.get('https://www.instagram.com/explore/')
    
    # Wait until the explore grid loads
    try:
        print("Loading..........")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//section//div[contains(@class, 'x78zum5 xdt5ytf x1iyjqo2 xdj266r xkrivgy x4n8cb0 x1gryazu x1ykew4q xh8yej3 x19b80pe xhae0no xmjrnx3 x16mfq2j x1e49onv x7flfwp x1ugxg0y x1oqrbt2 xgzdhx4')]"))
        )
        print("✅ Successfully navigated to Explore page.")        
        
    except Exception as e:
        print(f"❌ Failed to load Explore page: {e}")

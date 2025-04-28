from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def navigate_to_reels(driver):
    driver.get('https://www.instagram.com/reels/')

    try:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x1qjc9v5')]"))
        )
        
        print("Reel has been loaded successfully")
    except Exception as e:
        print(e)


 
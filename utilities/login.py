from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def login_to_instagram(driver):
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    
    wait = WebDriverWait(driver, 10)
    
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_input.send_keys(username)
    
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(password)
    
    password_input.submit()
    
    try:
        save_info_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Save info']"))
        )
        save_info_button.click()
        print("Clicked 'Save info' button.")
        
        # profile_side_button = WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/hisenberg638/')]"))
        # )
        # profile_side_button.click()
        
    except Exception as e:
        print("Couldn't find or click the 'Save info' button.")
        print(e)
        
    time.sleep(3)

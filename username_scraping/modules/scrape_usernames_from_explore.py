import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.navigate_to_explore import navigate_to_explore
import pandas as pd  # Importing pandas for saving to Excel

count = 0

# Function to scrape usernames from explore
def scrape_usernames_from_explore(driver):
    
    global count
    usernames = []
    
    try:
        # Navigate to Explore page
        navigate_to_explore(driver)
        click_post(driver)


        while True:
            count = count + 1
            print(count)
            if count == 50:
                driver.refresh()
                navigate_to_explore(driver)
                time.sleep(10)
                click_post(driver)
                count = 0
                
            username = fetch_username(driver)
            if username:
                if username not in usernames:
                    usernames.append(username)
                    print(f"✅Fetched username: {username}")
                    
                    # Save immediately after each new username
                    save_usernames_to_excel(usernames)
                else:
                    print(f"♻️Username '{username}' already scraped. Skipping.") 
            else:
                print("❌ Could not fetch username.")
            
            time.sleep(2)
            next_button_click(driver)
            # print(f"✅ Clicked the 'Next' button. ({c+1})")


    except KeyboardInterrupt:
        print("Stopped by user manually!")


    except Exception as e:
        print(f"❌ {e}")


def click_post(driver):
    clickable_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "_aagw"))
                )
    driver.execute_script("arguments[0].scrollIntoView(true);", clickable_div)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", clickable_div)
    # print("✅ Clicked on the post (div with class _aagw)")
        
        
def next_button_click(driver):
        next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//button[@class='_abl-'])[2]"))
                )
        next_button.click()
        

def fetch_username(driver):
    try:
        username_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[contains(@class, '_acan') and contains(@href, '/')]"
            ))
        )
        username = username_element.text
        return username
    except Exception as e:
        print(f"❌ Failed to fetch username: {e}")
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
        
        print("✅Updated 'usernames.xlsx' with new usernames!")
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def scroll_reel(driver):
    try:
        actions = ActionChains(driver)
        
        # Send Down key
        actions.send_keys(Keys.ARROW_DOWN).perform()
        
        # time.sleep(1)  # Wait for reel to load
    except Exception as e:
        print(f"Error while pressing Down key: {e}")

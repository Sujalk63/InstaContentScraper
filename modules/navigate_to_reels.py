from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_reels(driver):
    try:
        reels_tab = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/reels/')]"))
        )
        reels_tab.click()
        print("Clicked on 'Reels' tab.")
    except Exception as e:
        print("Couldn't find or click the 'Reels' tab.")
        print(e)

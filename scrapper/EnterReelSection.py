WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/reels/')]"))
)
    
try:
    # Wait for and click the Reels tab
    reels_tab = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/reels/']"))
    )
    reels_tab.click()
    print("Clicked on 'Reels' tab.")
except Exception as e:
    print("Couldn't find or click the 'Reels' tab.")
    print(e)


input("Press Enter to close the browser...")  # Wait for user input to close the browser
driver.quit() 
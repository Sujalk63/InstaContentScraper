import os
from selenium import webdriver                                       # Main tool from Selenium to control the browser.
from selenium.webdriver.chrome.service import Service                # Helps Selenium locate and manage the ChromeDriver executable.
from selenium.webdriver.common.by import By                          # Used to locate elements on the webpage (like by ID, class, tag, etc.).
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv  # Import the library
import time                                                          # allows you to pause the code

load_dotenv()

username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

# Path to your chromedriver.exe
driver_path = r'driver/chromedriver.exe'                             # Update with your path

service = Service(driver_path)                                       # tells selenium here's the path to the driver you need to use to control Chrome.
driver = webdriver.Chrome(service=service)                           #launchees the web browser

# Open a webpage and get instagram login page
driver.get('https://www.instagram.com/accounts/login/')

time.sleep(2)

# Wait until input fields appear
wait = WebDriverWait(driver, 10)                                      # Only waits until the element is found or timeout

username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
username_input.send_keys(username)
password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
password_input.send_keys(password)

password_input.submit()                                               # Submit via the password input field, typically users hit enter while being on the input filed however we can call submit independently

# print("submitted")

try:
    # Wait until the "Save info" button is clickable, then click it
    save_info_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, 
                                    "//button[text()='Save info']"
                                    ))                                 # EC.element_to_be_clickable checks if the element is clickable then proceeds
    )
    save_info_button.click()
    print("Clicked 'Save info' button.")
    profile_side_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/hisenberg638/']"))  # Corrected quotes inside XPath
    )
    profile_side_button.click()
except Exception as e:
    print("Couldn't find or click the 'Save info' button.")
    print(e)

input("Press Enter to close the browser...")  # Wait for user input to close the browser
driver.quit() 
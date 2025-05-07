from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # Importing pandas for saving to Excel
from hunting_data.modules.hunt_profile_data_functions import *

# from utilities.is_fetching_done import is_fetch_done # not optimized use load_done_status instead
from utilities.save_to_excel import save_profile_data_to_excel
from utilities.load_done_status import load_done_status

def scrape_content(driver):
    print("will work on it")
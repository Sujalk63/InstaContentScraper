from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.convert_to_number import convert_to_number
import pandas as pd  # Importing pandas for saving to Excel
from hunting_data.modules.hunt_profile_data_functions import *


def scrape_profiles(driver, usernames=None):


    """
    Scrapes Instagram profile data.
    If `usernames` is None, reads from usernames.xlsx.
    If `usernames` is a string, treats it as a single username.
    If `usernames` is a list, scrapes all usernames in the list.
    """
    if usernames is None:
        # Batch mode from Excel
        df = pd.read_excel("usernames_dummy.xlsx")
        usernames_list = df["Username"].dropna().unique().tolist()
    elif isinstance(usernames, str):
        # Single username mode
        usernames_list = [usernames.strip()]
    elif isinstance(usernames, list):
        usernames_list = [u.strip() for u in usernames if isinstance(u, str)]
    else:
        print("Invalid input format for usernames.")
        return

    for username in usernames_list:
        data = fetch_profile_data(driver, username)
        # time.sleep(60)
        


def fetch_profile_data(driver, username):
    url = f"https://www.instagram.com/{username}/"

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'xrvj5dj'))
        )
    except Exception as e:
        print(f"Profile page did not load properly for {username}: {e}")
        return None


    data = {
        "Username": username,
        "Full Name": None,
        "Number of Posts": None,
        "Followers Count": None,
        "Following Count": None,
        "Profile Bio": None,
        "Thread Link": None,
        "External Link": [],
        "Email in Bio": None,
        # "Collab/Mgmt Info": None,
        # "Business Category Label": None,
        "Profile Picture URL": None,
        "Is Verified": False,
        "Professional Label": None
    }

    try:
        
        fullName = get_full_name(driver)
        data["Full Name"] = fullName

        numberOfPosts = post_count(driver)
        data["Number of Posts"] = numberOfPosts

        followersCount = followers_count(driver)
        data["Followers Count"] = followersCount

        followingCount = following_count(driver)
        data["Following Count"] = followingCount
        
        profileBio = profile_bio(driver)
        data["Profile Bio"] = profileBio
        
        threadLink = thread_link(driver)
        data["Thread Link"] = threadLink

        externalLink = external_link(driver)
        data["External Link"] = externalLink
        
        email = extract_email_from_bio(profileBio)
        data["Email in Bio"] = email

        ppLink = pp_link(driver, username)
        data["Profile Picture URL"] = ppLink

        isVerified = is_verified(driver)
        data["Is Verified"] = isVerified

        professionalLabel = profession_label(driver)
        data["Professional Label"] = professionalLabel

        printing(data)

        
    except Exception as e:
        print(f"Error fetching {username}: {e}")

    return data



#     | Feature            | Absolute XPath                        | Relative XPath                             |
# |--------------------|----------------------------------------|--------------------------------------------|
# | Starts with        | `/`                                    | `//`                                       |
# | Depends on layout? | Yes (very fragile)                     | No (more flexible)                         |
# | Preferred for      | Debugging / quick test                 | Real-world scraping/automation             |
# | Example            | `/html/body/div[1]/div/div[2]/span`    | `//span[contains(@class, 'my-class')]`     |
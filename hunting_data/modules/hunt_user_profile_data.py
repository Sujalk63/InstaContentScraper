from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.convert_to_number import convert_to_number
import pandas as pd  # Importing pandas for saving to Excel
import re

t = 2

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
        
        # fullName = get_full_name(driver)
        # data["Full Name"] = fullName
        # print(f'{username}: {data["Full Name"]}')

        # numberOfPosts = post_count(driver)
        # data["Number of Posts"] = numberOfPosts
        # print(f'{username}: {data["Number of Posts"]}')

        # followersCount = followers_count(driver)
        # data["Followers Count"] = followersCount
        # print(f'{username}: {data["Followers Count"]}')

        # followingCount = following_count(driver)
        # data["Following Count"] = followingCount
        # print(f'{username}: {data["Following Count"]}')
        
        # profileBio = profile_bio(driver)
        # data["Profile Bio"] = profileBio
        # print(f'{username}: {data["Profile Bio"]}')
        
        # threadLink = thread_link(driver)
        # data["Thread Link"] = threadLink
        # print(f'{username}: {data["Thread Link"]}')

        # externalLink = external_link(driver)
        # data["External Link"] = externalLink
        # print(f'{username}: {data["External Link"]}')
        
        # email = extract_email_from_bio(profileBio)
        # data["Email in Bio"] = email
        # print(f'{username}: {data["Email in Bio"]}')

        # ppLink = pp_link(driver, username)
        # data["Profile Picture URL"] = ppLink
        # print(f'{username}: {data["Profile Picture URL"]}')

        isVerified = is_verified(driver)
        data["Is Verified"] = isVerified
        print(f'{username}: {data["Is Verified"]}')
        

    except Exception as e:
        print(f"Error fetching {username}: {e}")

    return data




# 1
def get_full_name(driver):
    """
    Extracts the full name from an Instagram profile page.
    Assumes driver is already on the user's profile.
    Returns the full name or None if not found.
    """
    try:
        full_name_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//header//section//div//span[contains(@class, "x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj")]'))
        )
        return full_name_elem.text.strip() if full_name_elem.text else None
    
    except Exception:
        return None
    

# 2  
def post_count(driver):
    try:
        post_count_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//ul//li[1]//span[contains(@class, "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs")]'))
        )
        post_count_elem_text = post_count_elem.text.strip()
        value = convert_to_number(post_count_elem_text)
        return value if value else None
    
    except Exception:
        return None 


# 3
def followers_count(driver):
    try:
        followers_count_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//ul//li[2]//span[contains(@class, "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs")]'))
        )
        followers_count_elem_text = followers_count_elem.text.strip()
        value = convert_to_number(followers_count_elem_text)
        return value if value else None
    
    except Exception:
        return None

#  4
def following_count(driver):
    try:
        following_count_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//ul//li[3]//span[contains(@class, "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs")]'))
        )
        following_count_elem_text = following_count_elem.text.strip()
        value = convert_to_number(following_count_elem_text)
        return value if value else None
    
    except Exception:
        return None
    
#5
def profile_bio(driver):
    try:
        bio_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//span//div//span[contains(@class, "_ap3a _aaco _aacu _aacx _aad7 _aade")]'))
        )
        bio_elem_text = bio_elem.text.strip()
        value = bio_elem_text
        return value if value else None
    
    except Exception:
        return None
    
#6
def thread_link(driver):
    try:
        thread_link_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//a//span[contains(@class, "x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1fhwpqd xo1l8bm x5n08af x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj")]'))
        )
        thread_link = thread_link_elem.text.strip()
        value = thread_link
        return value if value else None
    
    except Exception:
        return None
    
#7
def external_link(driver): # when fetching external links the browser need to be opened
    try:
        # Try to find and click the link button
        link_button = WebDriverWait(driver, t).until(
            EC.element_to_be_clickable((By.XPATH, '//section//button[@class=" _acan _acao _acas _aj1- _ap30"]'))
        )

        link_button.click()

    except Exception:
        # Button not found or not clickable
        # print("Link button not found or not clickable.")
        return []

    try:
        # After clicking, wait for the popup and get all <a> links
        popup_links = WebDriverWait(driver, t).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@role, "dialog")]//a'))
        )
        external_links = [link.get_attribute('href') for link in popup_links]
        # print("External Links Found:", external_links)
        return external_links

    except Exception:
        print("No links found in popup.")
        return []
    
# 8
def extract_email_from_bio(profileBio):
    if not profileBio:
        return None
    
    # Regex to match most email formats
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', profileBio)
    
    if match:
        return match.group(0)
    else:
        return None
    
# 9
def pp_link(driver, username):
    try:
        pp_link_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, f'//section//span//img[contains(@alt, "{username}")]'))
        )
        profile_pic_url = pp_link_elem.get_attribute('src')
        pp_link = profile_pic_url.strip()
        value = pp_link
        return value if value else None
    
    except Exception as e:
        print(e)
        return None
    
# 10
def is_verified(driver):
    try:
        verified_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[1]/div/div/svg/path'))
        )
        if verified_elem:
            return True
        else:
            return False
    
    except Exception as e:
        # print(e)
        return False












#     | Feature            | Absolute XPath                        | Relative XPath                             |
# |--------------------|----------------------------------------|--------------------------------------------|
# | Starts with        | `/`                                    | `//`                                       |
# | Depends on layout? | Yes (very fragile)                     | No (more flexible)                         |
# | Preferred for      | Debugging / quick test                 | Real-world scraping/automation             |
# | Example            | `/html/body/div[1]/div/div[2]/span`    | `//span[contains(@class, 'my-class')]`     |
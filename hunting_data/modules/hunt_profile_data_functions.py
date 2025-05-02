from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.convert_to_number import convert_to_number
from urllib.parse import urlparse, parse_qs, unquote
import pandas as pd  # Importing pandas for saving to Excel
import re
import time

t = 2

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
def external_link(driver):
    try:
        # Check if the multiple-link button exists
        link_buttons = driver.find_elements(By.XPATH, '//section//button[contains(@class, " _acan _acao _acas _aj1- _ap30")]')

        if link_buttons:
            link_buttons[0].click()

            popup_links = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@role, "dialog")]//a'))
            )
            external_links = [
                                decode_instagram_redirect(link.get_attribute('href')) 
                                for link in popup_links
                             ]
                             

        else:
            direct_link_elem = driver.find_element(By.CSS_SELECTOR, 'a[href^="https://l.instagram.com/?u="]')
            direct_link = decode_instagram_redirect(direct_link_elem.get_attribute('href'))
            external_links = [direct_link] if direct_link else []

        # Filter out unwanted meta or Threads links
        filtered_links = [
            link for link in external_links
            if "about.meta.com" not in link and "threads." not in link
        ]
        return filtered_links

    except Exception:
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
    
#  10
def is_verified(driver):
    try:
        verified_elem = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="Verified"].x1lliihq.x1n2onr6')
        return True if verified_elem else False
    except Exception:
        return False
    
def profession_label(driver):
    try:
        professional_label_elem = WebDriverWait(driver, t).until(
            EC.presence_of_element_located((By.XPATH, '//section//div[contains(@class, "_ap3a _aaco _aacu _aacy _aad6 _aade")]'))
        )
        professional_label = professional_label_elem.text.strip()
        value = professional_label
        return value if value else None
    
    except Exception:
        return None

# 12
def printing(data):
    for key, value in data.items():
        print(f'{data["Username"]} has {key}: {value}')

# 13
def decode_instagram_redirect(url):
    # print("Decoding URL:", url)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if 'u' in query:
        decoded = unquote(query['u'][0])
        # print("Decoded URL:", decoded)
        return decoded
    return url

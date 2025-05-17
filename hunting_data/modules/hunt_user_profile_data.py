from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # Importing pandas for saving to Excel
from hunting_data.modules.hunt_profile_data_functions import *

# from utilities.is_fetching_done import is_fetch_done # not optimized use load_done_status instead
from utilities.save_to_excel import save_data_to_excel
from utilities.load_done_status import load_done_status


def scrape_profiles(driver, usernames=None, batch_size=100):
    # print("working")
    """
    Scrapes Instagram profile data.
    If `usernames` is None, reads from usernames.xlsx.
    If `usernames` is a string, treats it as a single username.
    If `usernames` is a list, scrapes all usernames in the list.
    """
    if usernames is None:
        df = pd.read_excel("usernames.xlsx")
        usernames_list = df["Username"].dropna().unique().tolist()
    elif isinstance(usernames, str):
        usernames_list = [usernames.strip()]
    elif isinstance(usernames, list):
        usernames_list = [u.strip() for u in usernames if isinstance(u, str)]
    else:
        print("❌ Invalid input format for usernames.")
        return

    done_usernames = load_done_status(
        excel_path="usernames.xlsx", coloumn="is_profile_data_fetched"
    )
    profile_data_batch = []

    try:
        for i, username in enumerate(usernames_list):
            print(f"{username} {i}")
            if username in done_usernames:
                print(f"⏭️ Skipping {username} (already marked as Done)")
                continue

            data = fetch_profile_data(driver, username)

            if data is None:
                print(f"⚠️ {username} changed or deleted")
                mark_profile_done(username)
                continue

            profile_data_batch.append(data)
            

            if len(profile_data_batch) >= batch_size:
                save_data_to_excel(
                    profile_data_batch,
                    file_path="usernames_profile_data.xlsx",
                    table_name="profileDataTable",
                )
                print(f"✅ Saved batch of {batch_size} profiles to Excel.")
                for profile in profile_data_batch:
                    mark_profile_done(profile["Username"])
                profile_data_batch = []

    finally:
        if profile_data_batch:
            print(
                f"⚠️ Saving final unsaved batch of {len(profile_data_batch)} profiles."
            )
            save_data_to_excel(
                profile_data_batch,
                file_path="usernames_profile_data.xlsx",
                table_name="profileDataTable",
            )
            for profile in profile_data_batch:
                mark_profile_done(profile["Username"])


def fetch_profile_data(driver, username):
    # print("working from fetch")
    url = f"https://www.instagram.com/{username}/"

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "xrvj5dj"))
        )
    except Exception as e:
        print(f"❌ Profile page did not load properly for {username}: {e}")
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
        "Professional Label": None,
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

        mark_profile_done(username)

    except Exception as e:
        print(f"❌ Error fetching {username}: {e}")

    return data


def mark_profile_done(username, excel_path="usernames.xlsx"):
    mark_done(username, "is_profile_data_fetched", excel_path)


#     | Feature            | Absolute XPath                        | Relative XPath                             |
# |--------------------|----------------------------------------|--------------------------------------------|
# | Starts with        | `/`                                    | `//`                                       |
# | Depends on layout? | Yes (very fragile)                     | No (more flexible)                         |
# | Preferred for      | Debugging / quick test                 | Real-world scraping/automation             |
# | Example            | `/html/body/div[1]/div/div[2]/span`    | `//span[contains(@class, 'my-class')]`     |

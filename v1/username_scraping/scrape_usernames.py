import undetected_chromedriver as uc
from username_scraping.modules.scrape_usernames_from_reels import scrape_usernames_from_reels
from username_scraping.modules.scrape_usernames_from_explore import scrape_usernames_from_explore


def scrape_username(driver):
    print("\nChoose an option to scrape usernames:")
    print("1. Scrape from Reels")
    print("2. Scrape from Explore")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\nScraping usernames from Reels...\n")
        scrape_usernames_from_reels(driver)
    elif choice == "2":
        print("\nScraping usernames from Explore...\n")
        scrape_usernames_from_explore(driver)
    else:
        print("Invalid choice. Please enter 1 or 2.")

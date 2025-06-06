# 📊 InstaContentScraper: Your AI-Powered Analysis Tool

## 🚀 Why This Project?

As a data analyst passionate about understanding **what makes Instagram content go viral**, I found a major gap: there was **no structured, publicly available dataset** that provided comprehensive, scalable insights into Instagram reels, profiles, or content strategies.

Most available datasets were either:

- Too **small-scale** (manually curated or outdated),
- Or **lacking key attributes** like hashtags, profile insights, or engagement metrics.

So I decided to **build a real-time, scalable scraper** that automates the process of collecting high-value Instagram profile and content data for analysis and modeling.

## 📥 Installation
To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/Sujalk63/InstaContentScraper.git
cd InstaContentScraper
pip install -r requirements.txt
```

## 📈 Use Cases

- 🔍 **Data Analytics** on what makes content viral
- 🤖 **Training ML models** to predict engagement
- 📊 **Dashboards** to visualize content strategies
- 🧑‍💼 **Creator tools** for growth planning
- 🧪 **A/B Testing Ideas** for content optimization

## 🧰 Tech Stack

- **Python**: Core logic and data handling
- **Selenium (WebDriver)**: Automating browser interactions and data scraping
- **Pandas**: Data cleaning, manipulation, and storage
- **Excel (.xlsx)**: Output format for structured data tracking and reusability
- **.env & uc chrome**: Secure login credentials and cookies management

## 🎥 Demo (Click on the preview)

[![Watch the demo](https://img.youtube.com/vi/jRGzaSpdjKc/0.jpg)](https://www.youtube.com/watch?v=jRGzaSpdjKc)



## 🧠 Key Features

- 🔐 **Login Automation** with session persistence using cookies
- 🔍 **Scrapes Usernames from Explore & Reels**: Automatically collects new target usernames by scrolling through Instagram's Explore page and Reels section, ensuring a fresh and dynamic user base for analysis.
- 📄 **Scrapes Profile Data**: Full name, bio, followers, following, posts, verified badge, business label, links, email, thread links, external links and more.
- 🎞️ **Scrapes Reels/Post Data**: Likes, comments, hashtags, duration, caption, content type, date, time and more.
- 💾 **Saves Data to Excel**: All scraped profile details and content (posts & reels) are automatically saved into separate Excel files — `usernames_profile_data.xlsx` for profile data and `username_content_data.xlsx` for post/reel analytics.

- 🧠 **Intelligent Resume**: Skips already scraped usernames, allowing safe resume after interruption
- ⚠️ **Handles Edge Cases**: Skips deleted/renamed/private accounts without crashing
- ✅ **Progress Tracking**: Uses a status column to record which profiles are done (`Done`, `Not Found`, etc.)

## 🗃️ Data Output

### 📂 1. Profile-Level Data → `usernames_profile_data.xlsx`

Contains core information about each Instagram profile, such as:

- `Username`
- `Full Name`
- `Followers Count`
- `Following Count`
- `Number of Posts`
- `Profile Bio`
- `Is Verified`
- `Professional Label`
- `External Link`
- `Email in Bio`
- `Thread Link`
- `Profile Picture URL`
- `is_profile_data_fetched` (status tracking)



### 🎞️ 2. Content-Level Data → `username_content_data.xlsx`

Captures detailed post/reel-specific data for every profile, including:

- `Username`
- `Content Type` (Post / Reel / Carousel)
- `Post/Reel URL`
- `Caption`
- `Hashtags Used`
- `Date Posted`
- `Time Posted`
- `Likes Count`
- `Comments Count`
- `Shares Count` _(if available)_
- `Views Count` _(for reels)_
- `Video Duration` _(for reels)_
- `Video Quality (Resolution)` _(optional if extractable)_
- `Engagement Rate` _(to be calculated)_
- `Audio Used` _(if reel)_
- `Collab Tag` _(if post is a collaboration)_
- `Location Tag` _(if provided)_

## 🔄 How It Works

1. Reads usernames from an Excel file
2. Skips users already marked as `"Done"`
3. Opens Instagram profile using Selenium
4. Extracts profile attributes (with error handling for deleted/private users)
5. Saves data to Excel and updates progress
6. Can safely **pause/resume anytime** without redoing work

## 🛠 Developer Notes & Troubleshooting Tips

**Some important reminders while switching accounts or running the scraper:**

- ❌ **Delete `__pycache__` from the `utilities` folder** and **remove `insta_cookies.json` from the `cookies` folder** — old cached files can inject outdated login cookies and cause login failures or data mismatches.

- 📉 **If the script says "Close the browser..." but fails to save properly**, your Excel file may be corrupted or missing required columns.  
  👉 **Fix:** Just delete the Excel file — the script will recreate a fresh one automatically.

## ⚠️ Disclaimer

- This project is for **educational and research purposes only**.  
- Scraping Instagram data must comply with **Instagram's terms of service**.  
- Consider using official APIs for production or commercial use.

## 📌 Future Enhancements

- Add **content scraping** from Reels and Posts(On going)
- Store data in **MongoDB** for better scalability
- Integrate with **Tableau or Power BI** for instant dashboards
- Predict **engagement or virality** using ML
- Add **GUI or SaaS interface** for non-tech users



## 🙋‍♂️ Author

**Sujal Karmakar**, Data Analyst | Data Reporting | Data Analysis | Exploratory Data Analysis

- 📧 [sujalkarmakar6363@gmail.com](mailto:sujalkarmakar6363@gmail.com)
- 🌐 **LinkedIn**: Connect with me on [LinkedIn](https://www.linkedin.com/in/sujal-karmakar-b266ab25b/).



## 🌟 Show Your Support

If you find this project useful, please ⭐️ the repo and share your thoughts.  
Let’s build data tools that help creators grow smarter 🚀

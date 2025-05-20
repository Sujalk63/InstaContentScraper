import pandas as pd


# Read the 'done' status of usernames once
def load_done_status(excel_path, coloumn):
    try:
        df = pd.read_excel(excel_path)
        done_usernames = set(df[df[coloumn].str.lower() == "done"]["Username"])
        return done_usernames
    except Exception as e:
        print(f"Error loading done status: {e}")
        return set()


def load_scraped_content_ids(excel_path):
    try:
        df = pd.read_excel(excel_path)  # reads the first sheet by default
        if "content_id" not in df.columns:
            print("⚠️ 'content_id' column not found in the Excel file.")
            return set()
        content_ids = df["content_id"].dropna().unique().tolist()
        return set(content_ids)
    except FileNotFoundError:
        print("⚠️ Excel file not found. Starting with empty content ID set.")
        return set()
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return set()

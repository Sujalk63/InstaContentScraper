import pandas as pd

def is_fetch_done(username, excel_path):
    try:
        df = pd.read_excel(excel_path)
        row = df[df["Username"] == username]
        if not row.empty and str(row["is_profile_data_fetched"].values[0]).strip().lower() == "done":
            return True
        return False
    except Exception as e:
        print(f"Error checking if profile is done for {username}: {e}")
        return False
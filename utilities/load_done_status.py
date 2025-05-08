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

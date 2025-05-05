import os
import pandas as pd 
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

def save_profile_data_to_excel(data, file_path):
    """
    Saves a single profile's data to Excel.
    - If the file doesn't exist, creates it with headers.
    - If it does exist, appends the data.
    """
    new_row = pd.DataFrame([data])  # convert dict to DataFrame

    if not os.path.exists(file_path):
        # File doesn't exist, create it with headers
        new_row.to_excel(file_path, index=False)
        print(f"✅ Created new file and saved data for: {data['Username']}")
    else:
        # File exists, append data
        existing_df = pd.read_excel(file_path)
        
        if data["Username"] in existing_df["Username"].values:
            print(f"❌ Username {data['Username']} already exists in file. Skipping save.")
            return

        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        updated_df.to_excel(file_path, index=False)
        print(f"✅ Appended data for: {data['Username']}")
    
    try:
        wb = load_workbook(file_path)
        ws = wb.active

        max_row = ws.max_row
        max_col = ws.max_column
        table_range = f"A1:{chr(64+max_col)}{max_row}"

        table = Table(displayName="ProfileDataTable", ref=table_range)
        style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True, showColumnStripes=False)
        table.tableStyleInfo = style
        ws.add_table(table)

        wb.save(file_path)
        print("📊 Excel sheet formatted as a table.")
    except Exception as e:
        print(f"⚠️ Failed to format Excel file as table: {e}")
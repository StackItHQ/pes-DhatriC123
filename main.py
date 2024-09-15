



from sheets.google_sheets_service import read_sheet_data, write_sheet_data, append_sheet_data, delete_sheet_data
from database.mysql_connector import read_mysql_data, write_mysql_data, update_mysql_data, delete_mysql_data
import time
from threading import Thread

# Define the Google Sheets ID and range
SPREADSHEET_ID = '1nQbDJhh8KLZbAW8iJh3zRokKrz52XJHQJ4sU-TDUMBE'  # Replace with your actual Google Sheets ID
RANGE_NAME = 'Sheet1!A1:D'  # The range of cells to read/write data

def clean_and_validate_data(row):
    """Clean and validate a row of data."""
    id, name, age, city = row
    
    # Ensure id is a string
    id = str(id) if id else None
    
    # Clean name and city (strip whitespace)
    name = name.strip() if name else None
    city = city.strip() if city else None
    
    # Validate age: convert to int if possible, otherwise set to None
    try:
        age = int(age) if age else None
    except ValueError:
        age = None
    
    return id, name, age, city

def sync_data():
    # Step 1: Read data from both sources
    sheet_data = read_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    mysql_query = "SELECT id, name, age, city FROM your_table"
    mysql_data = read_mysql_data(mysql_query)

    # Step 2: Compare and update both sources
    sheet_dict = {row[0]: clean_and_validate_data(row) for row in sheet_data[1:] if len(row) >= 4}  # Skip header row
    mysql_dict = {str(row[0]): row[1:] for row in mysql_data}

    # Update MySQL with new or changed data from Google Sheets
    for sheet_id, sheet_row in sheet_dict.items():
        if sheet_id not in mysql_dict:
            query = "INSERT INTO your_table (id, name, age, city) VALUES (%s, %s, %s, %s)"
            write_mysql_data(query, sheet_row)
            print(f"Inserted new row with id {sheet_id} in MySQL")
        elif mysql_dict[sheet_id] != sheet_row[1:]:
            query = "UPDATE your_table SET name=%s, age=%s, city=%s WHERE id=%s"
            update_mysql_data(query, (*sheet_row[1:], sheet_id))
            print(f"Updated row with id {sheet_id} in MySQL")

    # Delete rows from MySQL that are not in Google Sheets
    for mysql_id in mysql_dict.keys():
        if mysql_id not in sheet_dict:
            query = "DELETE FROM your_table WHERE id=%s"
            delete_mysql_data(query % mysql_id)
            print(f"Deleted row with id {mysql_id} from MySQL")

    # Update Google Sheets with data from MySQL
    updated_mysql_data = read_mysql_data(mysql_query)
    
    # Clear existing data in Google Sheets
    delete_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    
    # Write headers
    headers = [['id', 'name', 'age', 'city']]
    write_sheet_data(SPREADSHEET_ID, f'{RANGE_NAME.split("!")[0]}!A1:D1', headers)
    
    # Append updated data
    append_sheet_data(SPREADSHEET_ID, RANGE_NAME, updated_mysql_data)
    print("Updated Google Sheets with latest MySQL data")

    print("Sync completed successfully!")

if __name__ == '__main__':
    sync_data()



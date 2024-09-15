



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

def watch_google_sheets():
    last_known_state = {}
    while True:
        current_state = {row[0]: clean_and_validate_data(row) for row in read_sheet_data(SPREADSHEET_ID, RANGE_NAME)[1:] if len(row) >= 4}
        
        # Check for changes
        for id, row in current_state.items():
            if id not in last_known_state or last_known_state[id] != row:
                # Update or insert in MySQL
                query = "INSERT INTO your_table (id, name, age, city) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, age=%s, city=%s"
                write_mysql_data(query, (*row, row[1], row[2], row[3]))
                print(f"Updated/Inserted row with id {id} in MySQL")
        
        # Check for deletions
        for id in last_known_state.keys() - current_state.keys():
            delete_mysql_data("DELETE FROM your_table WHERE id=%s" ,(id,))
            print(f"Deleted row with id {id} from MySQL")
        
        last_known_state = current_state
        time.sleep(5)  # Check every 5 seconds

def watch_mysql():
    last_known_state = {}
    while True:
        mysql_query = "SELECT id, name, age, city FROM your_table"
        current_state = {str(row[0]): clean_and_validate_data(row) for row in read_mysql_data(mysql_query)}
        
        # Check for changes or additions
        changes = []
        for id, row in current_state.items():
            if id not in last_known_state or last_known_state[id] != row:
                changes.append(list(row))
        
        if changes:
            # Clear existing data in Google Sheets
            delete_sheet_data(SPREADSHEET_ID, RANGE_NAME)
            
            # Write headers
            headers = [['id', 'name', 'age', 'city']]
            write_sheet_data(SPREADSHEET_ID, f'{RANGE_NAME.split("!")[0]}!A1:D1', headers)
            
            # Append all data (including changes)
            all_data = [list(row) for row in current_state.values()]
            append_sheet_data(SPREADSHEET_ID, RANGE_NAME, all_data)
            print(f"Updated Google Sheets with latest MySQL data")
        
        last_known_state = current_state
        time.sleep(5)  # Check every 5 seconds

if __name__ == '__main__':
    print("Starting real-time synchronization...")
    Thread(target=watch_google_sheets).start()
    Thread(target=watch_mysql).start()
    
    # Keep the main thread alive
    while True:
        time.sleep(1)



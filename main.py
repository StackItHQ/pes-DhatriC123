from sheets.google_sheets_service import read_sheet_data, write_sheet_data
from database.mysql_connector import read_mysql_data, write_mysql_data


# Define the Google Sheets ID and range
SPREADSHEET_ID = '1nQbDJhh8KLZbAW8iJh3zRokKrz52XJHQJ4sU-TDUMBE'  # Replace with your actual Google Sheets ID
RANGE_NAME = 'Sheet1!A1:D10'  # The range of cells to read/write data

def sync_mysql_to_sheets():
    # Read data from MySQL
    mysql_query = "SELECT id, name, age, city FROM your_table"
    mysql_data = read_mysql_data(mysql_query)

    # Write data to Google Sheets
    write_sheet_data(SPREADSHEET_ID, RANGE_NAME, mysql_data)
    print("Data synced from MySQL to Google Sheets!")

def sync_sheets_to_mysql():
    # Step 1: Read data from Google Sheets
    google_sheet_data = read_sheet_data(SPREADSHEET_ID, RANGE_NAME)

    # Step 2: Insert or update data in MySQL
    for row in google_sheet_data:
        if len(row) == 3:  # If name, age, and city are provided (no 'id')
            name, age, city = row[0], row[1], row[2]
            # Let MySQL handle the auto-increment for 'id'
            query = """
                INSERT INTO your_table (name, age, city)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                age=VALUES(age), city=VALUES(city)
            """
            write_mysql_data(query, (name, age, city))
        else:
            print(f"Skipping row with insufficient data: {row}")

    print("Data synced from Google Sheets to MySQL!")

def sync_addition_deletion():
    # Read data from both sources
    google_sheet_data = read_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    mysql_query = "SELECT id, name, age, city FROM your_table"
    mysql_data = read_mysql_data(mysql_query)

    # Step 1: Detect additions or updates in Google Sheets that need to be reflected in MySQL
    google_sheet_ids = [row[0] for row in google_sheet_data]
    mysql_ids = [row[0] for row in mysql_data]

    # Add or update MySQL based on Google Sheets changes
    for row in google_sheet_data:
        if len(row) >= 4:
            sheet_id, name, age, city = row[0], row[1], row[2], row[3]
            if sheet_id not in mysql_ids:  # New row to be inserted into MySQL
                query = """
                    INSERT INTO your_table (id, name, age, city)
                    VALUES (%s, %s, %s, %s)
                """
                write_mysql_data(query, (sheet_id, name, age, city))
            else:  # Existing row, update if necessary
                matching_row = next((mrow for mrow in mysql_data if mrow[0] == sheet_id), None)
                if matching_row and (matching_row[1:] != (name, age, city)):
                    query = """
                        UPDATE your_table SET name=%s, age=%s, city=%s WHERE id=%s
                    """
                    update_mysql_data(query, (name, age, city, sheet_id))
        else:
            print(f"Skipping row with insufficient data: {row}")

    # Step 2: Detect deletions from Google Sheets that need to be reflected in MySQL
    for row in mysql_data:
        mysql_id = row[0]
        if mysql_id not in google_sheet_ids:
            query = "DELETE FROM your_table WHERE id=%s"
            delete_mysql_data(query, (mysql_id,))
            print(f"Deleted row with id {mysql_id} from MySQL")

    # Step 3: Sync deletions in MySQL back to Google Sheets (if needed)
    google_sheet_ids = [row[0] for row in google_sheet_data]
    new_sheet_data = [row for row in google_sheet_data if row[0] in mysql_ids]
    
    # Overwrite Google Sheets with the updated data, removing deleted rows
    write_sheet_data(SPREADSHEET_ID, RANGE_NAME, new_sheet_data)
    
    print("Addition and deletion sync completed!")

# Main sync function for real-time sync of additions, updates, and deletions
def update_data_sync():
    # Sync data from Google Sheets to MySQL
    sync_sheets_to_mysql()

    # Sync data from MySQL to Google Sheets
    sync_mysql_to_sheets()

    # Sync additions and deletions
    sync_addition_deletion()

    print("Update sync completed!")




if __name__ == '__main__':
    # Uncomment one of the sync functions to run
    sync_sheets_to_mysql()  # Sync from Google Sheets to MySQL
    # sync_mysql_to_sheets()  # Sync from MySQL to Google Sheets


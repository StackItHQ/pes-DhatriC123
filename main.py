from sheets.google_sheets_service import read_sheet_data, write_sheet_data
from database.mysql_connector import read_mysql_data, write_mysql_data

# Define the Google Sheets ID and range
SPREADSHEET_ID = '1nQbDJhh8KLZbAW8iJh3zRokKrz52XJHQJ4sU-TDUMBE'  # Replace with your actual Google Sheets ID
RANGE_NAME = 'Sheet1!A1:D10'  # The range of cells to read/write data

# Example: Sync MySQL data to Google Sheets
def sync_mysql_to_sheets():
    # Step 1: Read data from MySQL
    mysql_query = "SELECT name, age, city FROM your_table"  # Adjust based on your table
    mysql_data = read_mysql_data(mysql_query)

    # Step 2: Write data to Google Sheets
    write_sheet_data(SPREADSHEET_ID, RANGE_NAME, mysql_data)
    print("Data successfully synced from MySQL to Google Sheets!")


def sync_sheets_to_mysql():
    # Step 1: Read data from Google Sheets
    google_sheet_data = read_sheet_data(SPREADSHEET_ID, RANGE_NAME)

    # Step 2: Insert data into MySQL
    for row in google_sheet_data:
        # Only proceed if the row has at least 3 columns
        if len(row) >= 3:
            values = (row[0], row[1], row[2])  # Assuming name, age, and city
            query = "INSERT INTO your_table (name, age, city) VALUES (%s, %s, %s)"
            write_mysql_data(query, values)
        else:
            print(f"Skipping row with insufficient data: {row}")
    
    print("Data successfully synced from Google Sheets to MySQL!")



if __name__ == '__main__':
    # Uncomment one of the sync functions to run
    sync_sheets_to_mysql()  # Sync from Google Sheets to MySQL
    # sync_mysql_to_sheets()  # Sync from MySQL to Google Sheets

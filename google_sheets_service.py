from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your downloaded service account JSON key
SERVICE_ACCOUNT_FILE = 'C:\\Users\\DHATRI C\\Desktop\\superjoin\\credentials.json'

# Define the scopes the application will use
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service

# Function to read data from Google Sheets
def read_sheet_data(spreadsheet_id, range_name):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    return rows

# Function to write data to Google Sheets
def write_sheet_data(spreadsheet_id, range_name, values):
    service = get_google_sheets_service()
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    return result

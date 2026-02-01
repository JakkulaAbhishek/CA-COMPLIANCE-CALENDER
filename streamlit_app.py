import streamlit as st
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# --- APP CONFIGURATION ---
st.set_page_config(page_title="CA Compliance Command Center", layout="wide")
st.title("⚖️ CA Compliance Calendar Automator (2025-26)")

# Google Calendar Scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Authenticates the user and returns the Google Calendar service object."""
    creds = None
    # token.pickle stores user's access/refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You must have a 'credentials.json' file from Google Cloud Console
            if not os.path.exists('credentials.json'):
                st.error("Missing 'credentials.json'. Please upload it to your project folder.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return build('calendar', 'v3', credentials=creds)

def create_compliance_event(service, title, date, description):
    """Creates an all-day event in the primary Google Calendar."""
    event = {
        'summary': f"📌 COMPLIANCE: {title}",
        'description': description,
        'start': {'date': date.strftime('%Y-%m-%d')},
        'end': {'date': (date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                {'method': 'popup', 'minutes': 60},      # 1 hour before
            ],
        },
    }
    service.events().insert(calendarId='primary', body=event).execute()

# --- INTERFACE ---
st.write("This app will automatically push all statutory due dates for FY 2025-26 to your Google Calendar.")

if st.button("🚀 Generate & Sync All Compliance Dates"):
    service = get_calendar_service()
    if service:
        year = 2025
        # Define Compliances
        # Monthly Filings
        for month in range(1, 13):
            # TDS Payment (7th of next month, April 30 for March)
            tds_day = 30 if month == 3 else 7
            tds_month = 4 if month == 3 else (month % 12) + 1
            create_compliance_event(service, "TDS Payment", datetime.date(year, month, tds_day), "Deposit TDS for previous month.")
            
            # GSTR-1 & PF/ESI
            create_compliance_event(service, "GSTR-1 (Monthly)", datetime.date(year, month, 11), "Filing outward supplies.")
            create_compliance_event(service, "PF & ESI Payment", datetime.date(year, month, 15), "Deposit PF/ESI contributions.")
            create_compliance_event(service, "GSTR-3B (Monthly)", datetime.date(year, month, 20), "Summary GST return.")

        # Quarterly/Annual Items
        compliances = [
            {"name": "TDS Return Filing (Q1)", "date": datetime.date(2025, 7, 31)},
            {"name": "TDS Return Filing (Q2)", "date": datetime.date(2025, 10, 31)},
            {"name": "Advance Tax (1st Inst.)", "date": datetime.date(2025, 6, 15)},
            {"name": "ITR Filing (Individuals)", "date": datetime.date(2025, 7, 31)},
            {"name": "ITR Filing (Companies/Audit)", "date": datetime.date(2025, 10, 31)},
            {"name": "GSTR-9 (Annual)", "date": datetime.date(2025, 12, 31)},
        ]
        
        for item in compliances:
            create_compliance_event(service, item['name'], item['date'], "Statutory deadline.")
            
        st.success("All compliance dates have been successfully synced to your calendar!")

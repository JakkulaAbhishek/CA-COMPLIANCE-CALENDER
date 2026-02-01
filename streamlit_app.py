import streamlit as st
import datetime
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# --- CONFIGURATION ---
st.set_page_config(page_title="CA Compliance Automator", page_icon="⚖️")
st.title("📅 CA Statutory Compliance Calendar")
st.write("Syncs TDS, GST, PF/ESI, and Income Tax deadlines to your Google Calendar.")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Authenticates using credentials.json from your project folder."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                st.error("⚠️ Error: 'credentials.json' not found. Please upload it to your project folder.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

def add_compliance_event(service, title, date, desc):
    """Helper to create all-day events."""
    event = {
        'summary': f"🚀 {title}",
        'description': desc,
        'start': {'date': date.strftime('%Y-%m-%d')},
        'end': {'date': (date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 60}]}
    }
    service.events().insert(calendarId='primary', body=event).execute()

# --- SYNC BUTTON ---
if st.button("Sync All 2025-26 Compliance Dates"):
    service = get_calendar_service()
    if service:
        year = 2025
        with st.spinner("Pushing dates to your calendar..."):
            # Monthly Tasks
            for m in range(1, 13):
                # TDS Payment (7th of next month, April 30 for March)
                tds_day = 30 if m == 3 else 7
                tds_month = 4 if m == 3 else (m % 12) + 1
                add_compliance_event(service, "TDS Payment", datetime.date(year, m, tds_day), "Monthly TDS deposit.")
                
                # GST, PF & ESI
                add_compliance_event(service, "GSTR-1 Filing", datetime.date(year, m, 11), "Monthly Outward Supplies.")
                add_compliance_event(service, "PF & ESI Payment", datetime.date(year, m, 15), "Statutory Labor Law payments.")
                add_compliance_event(service, "GSTR-3B Filing", datetime.date(year, m, 20), "Monthly Summary Return.")

            # Quarterly & Annual Deadlines
            special_dates = [
                ("TDS Return (Q1)", datetime.date(2025, 7, 31)),
                ("ITR - Individuals", datetime.date(2025, 7, 31)),
                ("ITR - Companies/Audit", datetime.date(2025, 10, 31)),
                ("Advance Tax (1st Inst.)", datetime.date(2025, 6, 15)),
                ("Advance Tax (2nd Inst.)", datetime.date(2025, 9, 15)),
                ("Advance Tax (3rd Inst.)", datetime.date(2025, 12, 15)),
                ("Advance Tax (4th Inst.)", datetime.date(2026, 3, 15)),
            ]
            for title, d in special_dates:
                add_compliance_event(service, title, d, "Filing Deadline.")

        st.success("✅ Success! All dates synced.")

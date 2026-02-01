import streamlit as st
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# --- SETTINGS ---
st.set_page_config(page_title="CA Compliance Calendar", page_icon="📅")
st.title("⚖️ All-in-One CA Compliance Automator")
st.markdown("Syncs TDS, GST, PF/ESI, and Income Tax deadlines to your Google Calendar.")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                st.error("Error: 'credentials.json' not found. Please upload it to your project.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

def add_event(service, summary, date, description):
    event = {
        'summary': f"📢 {summary}",
        'description': description,
        'start': {'date': date.strftime('%Y-%m-%d')},
        'end': {'date': (date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')},
        'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 60}]}
    }
    service.events().insert(calendarId='primary', body=event).execute()

# --- SYNC LOGIC ---
if st.button("Sync All 2025-26 Compliances"):
    service = get_calendar_service()
    if service:
        year = 2025
        with st.spinner("Syncing dates..."):
            for m in range(1, 13):
                # 1. TDS Payments (7th of next month; April 30 for March)
                tds_day = 30 if m == 3 else 7
                tds_month = 4 if m == 3 else (m % 12) + 1
                add_event(service, "TDS Payment Due", datetime.date(year, m, tds_day), "Monthly TDS deposit deadline.")

                # 2. Monthly GST (GSTR-1 & 3B)
                add_event(service, "GSTR-1 Filing", datetime.date(year, m, 11), "Monthly Outward Supplies.")
                add_event(service, "GSTR-3B Filing", datetime.date(year, m, 20), "Monthly Summary Return.")

                # 3. PF & ESI
                add_event(service, "PF & ESI Contribution", datetime.date(year, m, 15), "Statutory Labor Law payments.")

            # 4. Quarterly / Annual Deadlines
            special_dates = [
                ("TDS Return (Q1)", datetime.date(2025, 7, 31)),
                ("TDS Return (Q2)", datetime.date(2025, 10, 31)),
                ("TDS Return (Q3)", datetime.date(2026, 1, 31)),
                ("TDS Return (Q4)", datetime.date(2026, 5, 31)),
                ("ITR - Individuals (Non-Audit)", datetime.date(2025, 7, 31)),
                ("ITR - Companies & Audit Cases", datetime.date(2025, 10, 31)),
                ("Advance Tax - 1st Inst.", datetime.date(2025, 6, 15)),
                ("Advance Tax - 2nd Inst.", datetime.date(2025, 9, 15)),
                ("Advance Tax - 3rd Inst.", datetime.date(2025, 12, 15)),
                ("Advance Tax - 4th Inst.", datetime.date(2026, 3, 15)),
            ]
            for title, d in special_dates:
                add_event(service, title, d, "Statutory Filing Deadline.")

        st.success("Successfully added all compliance dates to your calendar!")

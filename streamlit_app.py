import smtplib
import schedule
import time
from datetime import date
from email.mime.text import MIMEText

# ========== USER CONFIG ==========
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Gmail App Password
REMIND_BEFORE_DAYS = 5

USER_EMAIL = input("Enter email for compliance reminders: ")

# ========== COMPLIANCE DATABASE ==========
COMPLIANCES = [

    # -------- MONTHLY --------
    {"name": "PF Payment", "type": "monthly", "day": 15},
    {"name": "ESI Payment", "type": "monthly", "day": 15},
    {"name": "GST GSTR-3B", "type": "monthly", "day": 20},
    {"name": "TDS Payment", "type": "monthly", "day": 7},

    # -------- QUARTERLY --------
    {"name": "TDS Return Q1", "type": "fixed", "month": 7, "day": 31},
    {"name": "TDS Return Q2", "type": "fixed", "month": 10, "day": 31},
    {"name": "TDS Return Q3", "type": "fixed", "month": 1, "day": 31},
    {"name": "TDS Return Q4", "type": "fixed", "month": 5, "day": 31},

    {"name": "GSTR-1 Quarterly", "type": "quarterly", "day": 13},

    # -------- GST ANNUAL --------
    {"name": "GSTR-9", "type": "fixed", "month": 12, "day": 31},
    {"name": "GSTR-9C", "type": "fixed", "month": 12, "day": 31},

    # -------- INCOME TAX --------
    {"name": "ITR Non-Audit", "type": "fixed", "month": 7, "day": 31},
    {"name": "Tax Audit Report", "type": "fixed", "month": 9, "day": 30},
    {"name": "ITR Audit", "type": "fixed", "month": 10, "day": 31},
    {"name": "Transfer Pricing 3CEB", "type": "fixed", "month": 11, "day": 30},

    # -------- ADVANCE TAX --------
    {"name": "Advance Tax 1", "type": "fixed", "month": 6, "day": 15},
    {"name": "Advance Tax 2", "type": "fixed", "month": 9, "day": 15},
    {"name": "Advance Tax 3", "type": "fixed", "month": 12, "day": 15},
    {"name": "Advance Tax 4", "type": "fixed", "month": 3, "day": 15},

    # -------- ROC --------
    {"name": "AOC-4 Filing", "type": "fixed", "month": 10, "day": 30},
    {"name": "MGT-7 Filing", "type": "fixed", "month": 11, "day": 30},

    # -------- OTHER --------
    {"name": "Form 103B (Audit Report Trusts)", "type": "fixed", "month": 9, "day": 30},
]

# ========== EMAIL FUNCTION ==========
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = USER_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# ========== DUE DATE CHECKER ==========
def check_compliances():
    today = date.today()

    for comp in COMPLIANCES:
        due = None

        if comp["type"] == "fixed":
            due = date(today.year, comp["month"], comp["day"])

        elif comp["type"] == "monthly":
            due = date(today.year, today.month, comp["day"])

        elif comp["type"] == "quarterly":
            if today.month in [1,4,7,10]:
                due = date(today.year, today.month, comp["day"])

        if not due:
            continue

        days_left = (due - today).days

        if 0 <= days_left <= REMIND_BEFORE_DAYS:
            subject = f"⚠️ {comp['name']} Due Soon"
            body = f"""
📢 Compliance Reminder

Compliance: {comp['name']}
Due Date: {due}
Days Left: {days_left}

Please complete before due date.

— CA Compliance System
"""
            send_email(subject, body)
            print(f"Reminder sent: {comp['name']}")

# ========== SCHEDULER ==========
schedule.every().day.at("09:00").do(check_compliances)

print("✅ CA Compliance Reminder Running...")
print("Checking daily at 9 AM...")

while True:
    schedule.run_pending()
    time.sleep(60)

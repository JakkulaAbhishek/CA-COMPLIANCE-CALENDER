import schedule
import time
from datetime import date, timedelta
from compliances import COMPLIANCES
from emailer import send_email

USER_EMAIL = input("Enter your email for reminders: ")

REMIND_BEFORE_DAYS = 5


def check_due_dates():
    today = date.today()

    for comp in COMPLIANCES:

        due = None

        # Annual fixed dates
        if "due_date" in comp:
            m, d = comp["due_date"]
            due = date(today.year, m, d)

        # Monthly
        elif comp.get("frequency") == "monthly":
            due = date(today.year, today.month, comp["due_day"])

        # Quarterly
        elif comp.get("frequency") == "quarterly":
            if today.month in [1,4,7,10]:
                due = date(today.year, today.month, comp["due_day"])

        if not due:
            continue

        days_left = (due - today).days

        if 0 <= days_left <= REMIND_BEFORE_DAYS:
            subject = f"⚠️ Compliance Due: {comp['name']}"
            body = f"""
Reminder!

{comp['name']} is due on {due}.

Only {days_left} days left.
Please complete on time.

— CA Compliance System
"""
            send_email(USER_EMAIL, subject, body)
            print(f"Reminder sent for {comp['name']}")


schedule.every().day.at("09:00").do(check_due_dates)

print("✅ Compliance Reminder Running...")

while True:
    schedule.run_pending()
    time.sleep(60)

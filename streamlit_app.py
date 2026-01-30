import streamlit as st
import pandas as pd
import calendar
from datetime import date

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Indian Festival Calendar (2026–2099)",
    page_icon="📅",
    layout="wide"
)

# ---------------- DARK UI ----------------
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}
.block-container {
    background-color: #000000;
    padding-top: 1.5rem;
}
h1, h2, h3 {
    color: #ffffff;
}
select, input {
    background-color: #000000 !important;
    color: #ffffff !important;
}
.calendar-box {
    background: #0f0f0f;
    border: 1px solid #2a2a2a;
    border-radius: 14px;
    padding: 18px;
    height: 140px;
}
.day {
    font-size: 22px;
    font-weight: 600;
}
.festival {
    font-size: 13px;
    color: #00ffcc;
}
.weekday {
    text-align: center;
    font-weight: 700;
    color: #aaaaaa;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FESTIVAL ENGINE ----------------
def get_festivals(year):
    """Major Indian festivals (fixed-date + approx movable)"""
    return {
        date(year, 1, 1): "New Year",
        date(year, 1, 26): "Republic Day 🇮🇳",
        date(year, 3, 25): "Holi",
        date(year, 4, 14): "Dr Ambedkar Jayanti",
        date(year, 8, 15): "Independence Day 🇮🇳",
        date(year, 10, 2): "Gandhi Jayanti",
        date(year, 10, 20): "Dussehra",
        date(year, 11, 1): "Diwali",
        date(year, 12, 25): "Christmas 🎄"
    }

# ---------------- HEADER ----------------
st.title("📅 Indian Festival Calendar")
st.caption("Ultra-clean | Dark Mode | 2026 – 2099")

# ---------------- CONTROLS ----------------
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("📆 Select Year", list(range(2026, 2100)))

with col2:
    month = st.selectbox(
        "🗓 Select Month",
        list(calendar.month_name)[1:]
    )

month_num = list(calendar.month_name).index(month)

# ---------------- CALENDAR DATA ----------------
cal = calendar.Calendar(calendar.SUNDAY)
month_days = cal.monthdatescalendar(year, month_num)
festivals = get_festivals(year)

# ---------------- WEEK HEADER ----------------
weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
cols = st.columns(7)
for i, day in enumerate(weekdays):
    cols[i].markdown(f"<div class='weekday'>{day}</div>", unsafe_allow_html=True)

# ---------------- CALENDAR GRID ----------------
for week in month_days:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day.month == month_num:
            fest = festivals.get(day, "")
            cols[i].markdown(
                f"""
                <div class='calendar-box'>
                    <div class='day'>{day.day}</div>
                    <div class='festival'>{fest}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            cols[i].markdown(
                "<div class='calendar-box'></div>",
                unsafe_allow_html=True
            )

# ---------------- FESTIVAL LIST ----------------
st.divider()
st.subheader("🎉 Festivals This Year")

fest_list = [
    {"Date": d.strftime("%d-%m-%Y"), "Festival": f}
    for d, f in festivals.items()
]

df = pd.DataFrame(fest_list).sort_values("Date")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ---------------- FOOTER ----------------
st.caption("⚫ Pure Black UI • ⚪ White Typography • 🚀 Streamlit Pro Build")

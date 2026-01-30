import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindVault Game",
    page_icon="🧠",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ---------------- DARK MODE UI ----------------
st.markdown("""
<style>

/* FULL BLACK BACKGROUND */
.stApp {
    background-color: #000000;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

/* REMOVE WHITE BLOCK */
.block-container {
    background-color: #000000;
}

/* CARDS */
.card {
    background: #111111;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #333333;
    margin-bottom: 20px;
}

/* HEADINGS */
.big {
    font-size: 34px;
    font-weight: 700;
    color: #ffffff;
}

/* SCORE */
.score {
    font-size: 22px;
    color: #00ff9c;
}

/* INPUTS */
input, textarea {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #555555 !important;
}

/* BUTTONS */
.stButton > button {
    background-color: #000000;
    color: #ffffff;
    border: 1px solid #ffffff;
    border-radius: 8px;
    padding: 0.5em 1.2em;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #ffffff;
    color: #000000;
}

/* SELECTBOX */
div[data-baseweb="select"] > div {
    background-color: #000000;
    color: #ffffff;
    border: 1px solid #555555;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='big'>🧠 MindVault – Dark Mode</div>", unsafe_allow_html=True)
st.write("Test your **logic, memory & reflex speed** ⚡")

st.markdown(f"<div class='score'>🎯 Score: {st.session_state.score}</div>", unsafe_allow_html=True)
st.divider()

# ---------------- MODE SELECT ----------------
mode = st.selectbox(
    "🎮 Select Game Mode",
    ["Quick Math", "Memory Pattern", "Reaction Speed"]
)

# ---------------- QUICK MATH ----------------
if mode == "Quick Math":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    a = random.randint(10, 99)
    b = random.randint(10, 99)
    operator = random.choice(["+", "-", "*"])

    question = f"{a} {operator} {b}"
    correct = eval(question)

    st.subheader("🧮 Solve Quickly")
    answer = st.number_input(f"{question} = ?", step=1)

    if st.button("Submit"):
        if answer == correct:
            st.success("✅ Correct!")
            st.session_state.score += 10
        else:
            st.error(f"❌ Wrong! Answer: {correct}")
            st.session_state.score -= 5
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MEMORY GAME ----------------
elif mode == "Memory Pattern":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧩 Memory Challenge")

    pattern = [random.randint(1, 9) for _ in range(5)]
    st.write("Memorize this 👀")
    st.code(" ".join(map(str, pattern)))

    time.sleep(3)
    st.write("Enter the pattern:")

    user_input = st.text_input("Numbers separated by space")

    if st.button("Check"):
        try:
            user_pattern = list(map(int, user_input.split()))
            if user_pattern == pattern:
                st.success("🧠 Perfect!")
                st.session_state.score += 15
            else:
                st.error(f"❌ Wrong! Pattern: {pattern}")
                st.session_state.score -= 5
        except:
            st.warning("⚠ Invalid input")
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- REACTION SPEED ----------------
elif mode == "Reaction Speed":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚡ Reaction Speed Test")

    if st.button("Start Test"):
        time.sleep(random.uniform(2, 5))
        st.session_state.start_time = time.time()
        st.warning("CLICK NOW!")

    if st.session_state.start_time:
        if st.button("CLICK!"):
            reaction = time.time() - st.session_state.start_time
            st.session_state.start_time = None

            st.info(f"⏱ Reaction Time: {reaction:.3f}s")

            if reaction < 0.4:
                st.success("🔥 Lightning Fast")
                st.session_state.score += 20
            elif reaction < 0.8:
                st.success("👍 Good")
                st.session_state.score += 10
            else:
                st.warning("🐢 Slow")
                st.session_state.score += 2

            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.divider()
st.caption("⚫ Pure Black UI • ⚪ White Text • 🚀 Built with Streamlit")

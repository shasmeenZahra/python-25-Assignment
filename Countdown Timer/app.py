import time                          # For adding delays in countdown
import streamlit as st               # Streamlit library for UI

# 🧾 Streamlit UI Setup
st.set_page_config(page_title="Countdown Timer", layout="centered")  # Set page title and layout
st.title("⏳ Advanced Countdown Timer")                               # App title at the top

# ⌨️ User input for countdown time
seconds = st.number_input("Enter time (seconds):", min_value=1, step=1, value=10)

# 📺 Placeholder to dynamically update the timer display
timer_placeholder = st.empty()

# 🎛️ Control Buttons
start = st.button("Start")
pause = st.button("Pause")
resume = st.button("Resume")
reset = st.button("Reset")

# 🧠 Session state initialization (preserve values during reruns)
if "running" not in st.session_state:
    st.session_state.running = False               # Is the timer currently running?
if "time_left" not in st.session_state:
    st.session_state.time_left = seconds           # Remaining time

# 🟢 Start Button Logic
if start:
    st.session_state.running = True
    st.session_state.time_left = seconds

# ⏸️ Pause Button Logic
if pause:
    st.session_state.running = False

# ▶️ Resume Button Logic
if resume:
    st.session_state.running = True

# 🔁 Reset Button Logic
if reset:
    st.session_state.running = False
    st.session_state.time_left = seconds

# 🕰️ Countdown Function: Updates the time every second if timer is running
def countdown():
    while st.session_state.time_left > 0 and st.session_state.running:
        mins, secs = divmod(st.session_state.time_left, 60)          # Convert to MM:SS format
        timer_placeholder.markdown(f"## {mins:02d}:{secs:02d}")      # Update timer on UI
        time.sleep(1)                                                # Wait for 1 second
        st.session_state.time_left -= 1                              # Decrease time by 1 sec
    if st.session_state.time_left == 0 and st.session_state.running:
        timer_placeholder.markdown("## 🎉 Time's Up!")               # Show alert when time is up
        st.session_state.running = False

# 🚀 Start countdown loop if timer is running
if st.session_state.running:
    countdown()

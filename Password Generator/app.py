import time                           # For countdown delay
import streamlit as st                # Streamlit UI framework

# 🖼️ Streamlit page configuration
st.set_page_config(page_title="Countdown Timer", layout="centered")
st.title("⏳ Advanced Countdown Timer")

# ⌨️ Get user input for seconds
seconds = st.number_input("Enter time (seconds):", min_value=1, step=1, value=10)

# 📺 Placeholder for updating the timer display
timer_placeholder = st.empty()

# 🎛️ Control buttons
start = st.button("Start")
pause = st.button("Pause")
resume = st.button("Resume")
reset = st.button("Reset")

# 💾 Session state to persist timer status across reruns
if "running" not in st.session_state:
    st.session_state.running = False
if "time_left" not in st.session_state:
    st.session_state.time_left = seconds

# 🟢 Start the timer
if start:
    st.session_state.running = True
    st.session_state.time_left = seconds

# ⏸️ Pause timer
if pause:
    st.session_state.running = False

# ▶️ Resume timer
if resume:
    st.session_state.running = True

# 🔁 Reset timer
if reset:
    st.session_state.running = False
    st.session_state.time_left = seconds

# 🕰️ Countdown function to update timer
def countdown():
    while st.session_state.time_left > 0 and st.session_state.running:
        mins, secs = divmod(st.session_state.time_left, 60)
        timer_placeholder.markdown(f"## {mins:02d}:{secs:02d}")  # Show time in MM:SS
        time.sleep(1)
        st.session_state.time_left -= 1
    if st.session_state.time_left == 0 and st.session_state.running:
        timer_placeholder.markdown("## 🎉 Time's Up!")
        st.session_state.running = False

# ⬇️ Run countdown if timer is active
if st.session_state.running:
    countdown()

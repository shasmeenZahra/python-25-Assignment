# Importing necessary libraries
import streamlit as st        # Streamlit is used to create interactive web apps
import time                   # Time module is used here just in case we want to add delays (currently not used)

# Title and instruction for the user
st.title("🤖 Computer Guesses Your Number!")
st.write("Think of a number between 1 and 100, and I will try to guess it!")

# Initialize session state variables (preserve values between user interactions)
if "low" not in st.session_state:
    st.session_state.low = 1                               # Lower bound of guessing range
    st.session_state.high = 100                            # Upper bound of guessing range
    st.session_state.guess = (1 + 100) // 2                # First guess (middle of range)
    st.session_state.attempts = 0                          # Counter for number of attempts
    st.session_state.message = "Is this your number?"      # Message to display on success
    st.session_state.game_over = False                     # Flag to indicate if game has ended

# Game is active
if not st.session_state.game_over:
    # Display the current guessing range and the computer's guess
    st.subheader(f"🔢 Guessing between {st.session_state.low} and {st.session_state.high}")
    st.subheader(f"🤔 Is your number {st.session_state.guess}?")

    # Create 3 buttons for user feedback
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔼 Too Low"):
            # Adjust the lower bound and increase attempts
            st.session_state.low = st.session_state.guess + 1
            st.session_state.attempts += 1

    with col2:
        if st.button("✅ Correct!"):
            # Show success message and mark game as over
            st.session_state.message = f"🎉 Yay! I guessed your number in {st.session_state.attempts} attempts!"
            st.session_state.game_over = True

    with col3:
        if st.button("🔽 Too High"):
            # Adjust the upper bound and increase attempts
            st.session_state.high = st.session_state.guess - 1
            st.session_state.attempts += 1

    # Update guess if valid range remains, otherwise show error
    if st.session_state.low <= st.session_state.high:
        st.session_state.guess = (st.session_state.low + st.session_state.high) // 2
    else:
        st.error("Oops! Something went wrong. Please restart the game.")
        st.session_state.game_over = True

# Game has ended
else:
    st.balloons()  # Celebrate with balloons animation
    st.success(st.session_state.message)  # Show success message
    st.progress(st.session_state.attempts / 10)  # Visual progress bar (assuming success in max 10 tries)

    # Button to restart the game
    if st.button("🔄 Play Again"):
        # Reset all session state variables to start fresh
        st.session_state.low = 1
        st.session_state.high = 100
        st.session_state.guess = (1 + 100) // 2
        st.session_state.attempts = 0
        st.session_state.message = "Is this your number?"
        st.session_state.game_over = False
        st.rerun()  # Force rerun of the script

# Import necessary libraries
import streamlit as st  # For creating the web interface
import random           # To let the computer make random choices

# Title and game description
st.title("✊ Rock, 📄 Paper, ✂️ Scissors Game!")
st.write("Play against the computer and see who wins!")

# Define possible choices and corresponding emojis
choices = ["Rock", "Paper", "Scissors"]
emojis = {"Rock": "✊", "Paper": "📄", "Scissors": "✂️"}

# Initialize session state variables for storing scores
if "user_score" not in st.session_state:
    st.session_state.user_score = 0            # User's score
    st.session_state.computer_score = 0        # Computer's score

# Let the user choose their move using radio buttons
user_choice = st.radio("Choose your move:", choices, horizontal=True)

# When the 'Play' button is clicked
if st.button("🎮 Play"):
    # Computer randomly selects one of the choices
    computer_choice = random.choice(choices)

    # Game Logic: Determine the winner
    if user_choice == computer_choice:
        result = "It's a Draw! 🤝"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = "🎉 You Win!"
        st.session_state.user_score += 1  # Update user score
    else:
        result = "😢 Computer Wins!"
        st.session_state.computer_score += 1  # Update computer score

    # Display both choices and the result
    st.subheader(f"You chose: {emojis[user_choice]}   |   Computer chose: {emojis[computer_choice]}")
    st.success(result)

# Display the current score in the sidebar
st.sidebar.header("📊 Scoreboard")
st.sidebar.write(f"🧑 Your Score: {st.session_state.user_score}")
st.sidebar.write(f"🤖 Computer Score: {st.session_state.computer_score}")

# Restart button to reset scores
if st.button("🔄 Restart Game"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.rerun()  # Refresh the app to clear selections

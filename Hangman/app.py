# Import necessary libraries
import random  # For selecting random words randomly
import streamlit as st  # For building the interactive web interface

# Function to return a random word based on selected difficulty
def get_word(difficulty):
    """Returns a random word based on the selected difficulty."""
    words = {
        'easy': ['apple', 'ball', 'cat', 'dog', 'fish'],
        'medium': ['python', 'rocket', 'jungle', 'laptop', 'mobile'],
        'hard': ['elephant', 'avalanche', 'dictionary', 'university', 'javascript']
    }
    return random.choice(words[difficulty])

# Function to display hangman stage based on attempts left
def display_hangman(attempts):
    """Returns the hangman stage based on remaining attempts."""
    stages = ["🪂", "😵", "😨", "😰", "😥", "😧", "😀"]  # From lost to healthy
    return stages[attempts]

# Main function to control the game
def main():
    st.title("🎯 Hangman Game")

    # Initialize session state variables (to maintain game state)
    if 'word' not in st.session_state:
        st.session_state.word = ""  # The hidden word to guess
        st.session_state.word_letters = set()  # Letters yet to guess
        st.session_state.guessed_letters = set()  # Letters already guessed
        st.session_state.attempts = 6  # Total incorrect attempts allowed
        st.session_state.difficulty = ""  # Difficulty level

    # Start screen: select difficulty and start the game
    if st.session_state.word == "":
        st.subheader("🧩 Choose Difficulty")
        difficulty = st.radio("Select difficulty:", ('easy', 'medium', 'hard'))

        if st.button("Start Game"):
            st.session_state.word = get_word(difficulty)  # Get random word
            st.session_state.word_letters = set(st.session_state.word)
            st.session_state.difficulty = difficulty
            st.rerun()  # Restart UI to show guessing interface

    else:
        # Game is ongoing
        st.subheader("🔠 Guess the Word")
        st.write(display_hangman(st.session_state.attempts))  # Show current hangman face

        # Show word progress (guessed letters and underscores)
        st.write("Word:", " ".join([
            letter if letter in st.session_state.guessed_letters else '_'
            for letter in st.session_state.word
        ]))

        # Alphabet buttons for guessing
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        cols = st.columns(9)  # Layout: 9 columns for better UI

        for index, letter in enumerate(alphabet):
            with cols[index % 9]:  # Place buttons evenly across columns
                if st.button(letter):
                    if letter in st.session_state.guessed_letters:
                        st.warning("⚠️ You already guessed that letter!")
                    elif letter in st.session_state.word_letters:
                        # Correct guess
                        st.session_state.word_letters.remove(letter)
                        st.session_state.guessed_letters.add(letter)
                    else:
                        # Incorrect guess
                        st.session_state.attempts -= 1
                        st.session_state.guessed_letters.add(letter)
                    st.rerun()  # Update UI after each guess

        # Game win condition
        if not st.session_state.word_letters:
            st.success(f"🎉 Congratulations! You guessed the word: **{st.session_state.word}**")
            if st.button("🔁 Play Again"):
                st.session_state.word = ""  # Reset word to restart game
                st.rerun()

        # Game over condition
        elif st.session_state.attempts == 0:
            st.error(f"💀 Game Over! The correct word was: **{st.session_state.word}**")
            if st.button("🔁 Try Again"):
                st.session_state.word = ""  # Reset for a new game
                st.rerun()

# Run the game only when script is executed (not imported)
if __name__ == "__main__":
    main()

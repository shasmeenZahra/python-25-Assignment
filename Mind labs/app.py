# Streamlit library import kar rahe hain jo Python mein web apps banane ke liye use hoti hai
import streamlit as st

# Ek function define kar rahe hain jiska naam hai mad_libs
def mad_libs():
    # Page ka title set kar rahe hain
    st.title("Mad Libs Game")

    # User ko instruction de rahe hain
    st.write("Fill in the blanks to create a funny story!")

    # Input fields banaye hain jahan user ek noun (ism), verb (fail), adjective (sift) aur place (jagah) de sakta hai
    noun = st.text_input("Enter a noun:")            # Jaise 'cat', 'car', 'bottle' etc.
    verb = st.text_input("Enter a verb:")            # Jaise 'run', 'eat', 'dance' etc.
    adjective = st.text_input("Enter an adjective:") # Jaise 'funny', 'tall', 'angry' etc.
    place = st.text_input("Enter a place:")          # Jaise 'park', 'school', 'moon' etc.

    # Button create kiya hai "Generate Story" naam ka
    if st.button("Generate Story"):
        # Check kar rahe hain ke sab fields fill ki gayi hain
        if noun and verb and adjective and place:
            # User ke input se ek story create kar rahe hain
            story = f"One day, a {adjective} {noun} decided to {verb} at {place}. It was the most hilarious thing ever!"
            
            # Story ka heading show kar rahe hain
            st.subheader("Here is your Mad Libs story:")
            
            # Story ko display kar rahe hain
            st.write(story)
        else:
            # Agar koi field blank ho to warning show karte hain
            st.warning("Please fill in all the fields to generate the story.")

# Ye part ensure karta hai ke jab file directly run ki jaye to mad_libs() function call ho
if __name__ == "__main__":
    mad_libs()

import streamlit as st
import random
from collections import defaultdict

def build_markov_chain(text, n=2):
    """Build a Markov Chain model from the input text"""
    words = text.split()
    markov_chain = defaultdict(list)
    
    for i in range(len(words) - n):
        key = tuple(words[i:i + n])  # Create key as n-gram tuple
        markov_chain[key].append(words[i + n])  # Store next possible word
    
    return markov_chain

def generate_text(chain, seed, length=50):
    """Generate text using Markov Chain"""
    if seed not in chain:
        return "Seed phrase not found in text corpus. Try another one."
    
    result = list(seed)
    for _ in range(length):
        next_words = chain.get(tuple(result[-len(seed):]), [])
        if not next_words:
            break
        result.append(random.choice(next_words))
    
    return ' '.join(result)

def main():
    st.title("Markov Chain Text Composer")  # App title
    
    # User input for training text
    user_text = st.text_area("Enter training text:", "Once upon a time in a land far away...")
    n_gram = st.slider("Select n-gram size:", 1, 5, 2)
    
    if st.button("Build Model"):
        markov_chain = build_markov_chain(user_text, n_gram)
        st.session_state['markov_chain'] = markov_chain  # Store model in session state
        st.success("Markov Chain model built successfully!")
    
    # Text generation section
    if 'markov_chain' in st.session_state:
        seed_text = st.text_input("Enter seed phrase:")
        text_length = st.slider("Generated text length:", 10, 100, 50)
        
        if st.button("Generate Text"):
            seed_tuple = tuple(seed_text.split()[:n_gram])
            generated_text = generate_text(st.session_state['markov_chain'], seed_tuple, text_length)
            st.write("### Generated Text:")
            st.write(generated_text)

if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import time

# Function to perform binary search with step tracking
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    steps = []  # To store steps for visualization
    
    while low <= high:
        mid = (low + high) // 2  # Finding the middle index
        steps.append((low, mid, high))  # Storing current state
        
        if arr[mid] == target:
            return mid, steps  # Target found, return index and steps
        elif arr[mid] < target:
            low = mid + 1  # Narrowing search to the right half
        else:
            high = mid - 1  # Narrowing search to the left half
    
    return -1, steps  # Target not found

# Streamlit App for Binary Search Visualization
def main():
    st.title("Binary Search Visualization")  # App title
    
    # Slider to select array size dynamically
    array_size = st.slider("Select array size", 5, 30, 10)
    
    # Generating a sorted random array
    arr = sorted(np.random.randint(1, 100, array_size))
    
    # Input box to enter the number to search
    target = st.number_input("Enter number to search", min_value=1, max_value=100, value=arr[array_size // 2])
    
    if st.button("Search"):  # Search button
        index, steps = binary_search(arr, target)  # Perform binary search
        
        st.write(f"Array: {arr}")  # Display the array
        
        # Displaying search steps
        for step in steps:
            low, mid, high = step
            st.write(f"Low: {low}, Mid: {mid}, High: {high}")
            time.sleep(0.5)  # Adding delay for better visualization
        
        # Display search result
        if index != -1:
            st.success(f"Found {target} at index {index}")
        else:
            st.error(f"{target} not found in array")

# Running the app
if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import time
import random

# Game Constants
grid_size = 10
delay = 0.2  # Speed of snake movement

def init_game():
    """Initialize game variables."""
    st.session_state.snake = [(5, 5)]  # Starting position
    st.session_state.food = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    st.session_state.direction = "RIGHT"
    st.session_state.game_over = False
    st.session_state.score = 0

def move_snake():
    """Move the snake based on the current direction."""
    if st.session_state.game_over:
        return
    
    head_x, head_y = st.session_state.snake[-1]
    
    if st.session_state.direction == "UP":
        head_x -= 1
    elif st.session_state.direction == "DOWN":
        head_x += 1
    elif st.session_state.direction == "LEFT":
        head_y -= 1
    elif st.session_state.direction == "RIGHT":
        head_y += 1
    
    new_head = (head_x, head_y)
    
    # Check for collisions
    if new_head in st.session_state.snake or not (0 <= head_x < grid_size and 0 <= head_y < grid_size):
        st.session_state.game_over = True
        return
    
    st.session_state.snake.append(new_head)
    
    # Check if food is eaten
    if new_head == st.session_state.food:
        st.session_state.food = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        st.session_state.score += 1  # Increase score
    else:
        st.session_state.snake.pop(0)  # Remove tail

def draw_grid():
    """Draw the game grid."""
    grid = np.zeros((grid_size, grid_size), dtype=int)
    for x, y in st.session_state.snake:
        grid[x, y] = 1
    fx, fy = st.session_state.food
    grid[fx, fy] = 2
    
    st.write(f"### Score: {st.session_state.score}")
    st.write("Snake Game:")
    for row in grid:
        st.text(" ".join(["🟩" if cell == 1 else "🍎" if cell == 2 else "⬜" for cell in row]))

st.title("🐍Snake Game")

if "snake" not in st.session_state:
    init_game()

# Real-time controls using session state keys
key = st.text_input("Use W/A/S/D keys for movement (press Enter after input)")
if key:
    key = key.upper()
    if key == "W":
        st.session_state.direction = "UP"
    elif key == "S":
        st.session_state.direction = "DOWN"
    elif key == "A":
        st.session_state.direction = "LEFT"
    elif key == "D":
        st.session_state.direction = "RIGHT"

if st.button("Restart Game"):
    init_game()

draw_grid()

while not st.session_state.game_over:
    time.sleep(delay)
    move_snake()
    draw_grid()
    st.rerun()

if st.session_state.game_over:
    st.error(f"Game Over! Your Score: {st.session_state.score}. Press Restart to Play Again.")

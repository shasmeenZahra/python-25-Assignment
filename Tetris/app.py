import streamlit as st
import numpy as np
import time
import random

# Define the Tetris grid size
grid_height = 20
grid_width = 10

def init_game():
    """Initialize game variables."""
    st.session_state.grid = np.zeros((grid_height, grid_width), dtype=int)
    st.session_state.piece = get_random_piece()
    st.session_state.piece_position = [0, grid_width // 2 - 1]
    st.session_state.game_over = False
    st.session_state.score = 0

def get_random_piece():
    """Generate a random Tetris piece."""
    pieces = [
        np.array([[1, 1, 1, 1]]),  # I piece
        np.array([[1, 1], [1, 1]]),  # O piece
        np.array([[0, 1, 0], [1, 1, 1]]),  # T piece
        np.array([[1, 1, 0], [0, 1, 1]]),  # S piece
        np.array([[0, 1, 1], [1, 1, 0]]),  # Z piece
        np.array([[1, 0, 0], [1, 1, 1]]),  # L piece
        np.array([[0, 0, 1], [1, 1, 1]]),  # J piece
    ]
    return random.choice(pieces)

def draw_grid():
    """Render the Tetris grid in Streamlit."""
    grid_display = st.session_state.grid.copy()
    piece = st.session_state.piece
    x, y = st.session_state.piece_position
    
    # Place the current piece in the grid display
    for i in range(piece.shape[0]):
        for j in range(piece.shape[1]):
            if piece[i, j]:
                grid_display[x + i, y + j] = 1
    
    st.write("### Score: ", st.session_state.score)
    st.dataframe(grid_display, use_container_width=True)

def move_piece(dx, dy):
    """Move the current piece if possible."""
    if not st.session_state.game_over:
        st.session_state.piece_position[0] += dx
        st.session_state.piece_position[1] += dy

def drop_piece():
    """Drop the piece down by one step."""
    move_piece(1, 0)

def rotate_piece():
    """Rotate the current piece clockwise."""
    st.session_state.piece = np.rot90(st.session_state.piece, -1)

def place_piece():
    """Lock the piece into the grid."""
    piece = st.session_state.piece
    x, y = st.session_state.piece_position
    for i in range(piece.shape[0]):
        for j in range(piece.shape[1]):
            if piece[i, j]:
                st.session_state.grid[x + i, y + j] = 1
    st.session_state.piece = get_random_piece()
    st.session_state.piece_position = [0, grid_width // 2 - 1]

def check_game_over():
    """Check if new piece placement is blocked."""
    if np.any(st.session_state.grid[0] != 0):
        st.session_state.game_over = True

def game_loop():
    """Main game loop."""
    while not st.session_state.game_over:
        time.sleep(0.5)
        drop_piece()
        draw_grid()
        st.rerun()
    st.error("Game Over! Refresh to restart.")

st.title("🎮 Streamlit Tetris Game")

if "grid" not in st.session_state:
    init_game()

col1, col2, col3, col4 = st.columns(4)
if col1.button("⬅ Left"):
    move_piece(0, -1)
if col2.button("➡ Right"):
    move_piece(0, 1)
if col3.button("⬆ Rotate"):
    rotate_piece()
if col4.button("⬇ Drop"):
    drop_piece()

draw_grid()
if st.button("Start Game"):
    game_loop()

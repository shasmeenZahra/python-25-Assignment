import streamlit as st
import numpy as np
import random

# Define the Minesweeper grid size
grid_size = 10
num_mines = 15

def init_game():
    """Initialize game variables."""
    st.session_state.grid = np.zeros((grid_size, grid_size), dtype=int)
    st.session_state.revealed = np.full((grid_size, grid_size), False, dtype=bool)
    st.session_state.mines = set()
    st.session_state.game_over = False
    st.session_state.score = 0
    
    # Place mines randomly
    while len(st.session_state.mines) < num_mines:
        x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        st.session_state.mines.add((x, y))
        st.session_state.grid[x, y] = -1  # -1 represents a mine
    
    # Calculate adjacent mine counts
    for x in range(grid_size):
        for y in range(grid_size):
            if (x, y) in st.session_state.mines:
                continue
            count = sum((nx, ny) in st.session_state.mines for nx in range(x-1, x+2) for ny in range(y-1, y+2)
                        if 0 <= nx < grid_size and 0 <= ny < grid_size)
            st.session_state.grid[x, y] = count

def reveal_cell(x, y):
    """Reveal a cell and process the game logic."""
    if st.session_state.game_over or st.session_state.revealed[x, y]:
        return
    
    st.session_state.revealed[x, y] = True
    
    if (x, y) in st.session_state.mines:
        st.session_state.game_over = True
        st.error("Game Over! You hit a mine.")
    else:
        st.session_state.score += 1
        if st.session_state.grid[x, y] == 0:
            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if 0 <= nx < grid_size and 0 <= ny < grid_size:
                        reveal_cell(nx, ny)

def draw_grid():
    """Render the Minesweeper grid in Streamlit."""
    grid_display = np.full((grid_size, grid_size), "⬜", dtype=object)
    for x in range(grid_size):
        for y in range(grid_size):
            if st.session_state.revealed[x, y]:
                if (x, y) in st.session_state.mines:
                    grid_display[x, y] = "💣"
                else:
                    grid_display[x, y] = str(st.session_state.grid[x, y])
    
    st.write(f"### Score: {st.session_state.score}")
    st.write("#### Minesweeper:")
    st.dataframe(grid_display, use_container_width=True)

def game_loop():
    """Main game loop."""
    draw_grid()
    for x in range(grid_size):
        cols = st.columns(grid_size)
        for y in range(grid_size):
            if cols[y].button(f"({x},{y})"):
                if 0 <= x < grid_size and 0 <= y < grid_size:  # Ensure valid bounds
                    reveal_cell(x, y)
                    st.rerun()
    
    if st.session_state.game_over:
        st.error("Game Over! Press Restart to Play Again.")

st.title("💣 Minesweeper")

if "grid" not in st.session_state:
    init_game()

draw_grid()
if st.button("Restart Game"):
    init_game()
    st.rerun()

game_loop()

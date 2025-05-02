import numpy as np
import streamlit as st

def create_board():
    return np.zeros((6, 7), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(5, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(7 - 3):
        for r in range(6):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    
    for c in range(7):
        for r in range(6 - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    
    for c in range(7 - 3):
        for r in range(6 - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    
    for c in range(7 - 3):
        for r in range(3, 6):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    
    return False

st.title("Connect Four - Streamlit Edition")

if "board" not in st.session_state:
    st.session_state.board = create_board()
    st.session_state.turn = 0
    st.session_state.game_over = False

st.write("### Game Board")
st.dataframe(np.flip(st.session_state.board, 0))

if not st.session_state.game_over:
    col = st.number_input("Select a column (0-6):", min_value=0, max_value=6, step=1)
    if st.button("Drop Piece"):
        if is_valid_location(st.session_state.board, col):
            row = get_next_open_row(st.session_state.board, col)
            drop_piece(st.session_state.board, row, col, st.session_state.turn + 1)
            
            if winning_move(st.session_state.board, st.session_state.turn + 1):
                st.session_state.game_over = True
                st.success(f"Player {st.session_state.turn + 1} wins!")
            
            st.session_state.turn = (st.session_state.turn + 1) % 2
        else:
            st.warning("Invalid move. Try again.")

if st.session_state.game_over:
    if st.button("Restart Game"):
        st.session_state.board = create_board()
        st.session_state.turn = 0
        st.session_state.game_over = False
        st.experimental_rerun()

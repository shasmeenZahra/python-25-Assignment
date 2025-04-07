import streamlit as st
import numpy as np

# ✅ Function to create a blank 3x3 board
def initialize_board():
    return np.full((3, 3), "", dtype=str)

# ✅ Function to check if there's a winner or a draw
def check_winner(board):
    # Check rows
    for row in board:
        if all(row == row[0]) and row[0] != "":
            return row[0]

    # Check columns
    for col in board.T:  # .T transposes the board
        if all(col == col[0]) and col[0] != "":
            return col[0]

    # Check main diagonal
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != "":
        return board[0, 0]

    # Check anti-diagonal
    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != "":
        return board[0, 2]

    # Check for draw (no empty cell left)
    if "" not in board:
        return "Draw"

    return None  # No winner yet

# ✅ Minimax algorithm to calculate best move for AI
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif winner == "Draw":
        return 0

    if is_maximizing:  # AI turn (maximize score)
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board[i, j] = "O"  # Try move
                    score = minimax(board, depth + 1, False)
                    board[i, j] = ""  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:  # Player turn (minimize score)
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board[i, j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i, j] = ""
                    best_score = min(score, best_score)
        return best_score

# ✅ Function for AI to choose the best move
def best_move(board):
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == "":
                board[i, j] = "O"  # Try AI move
                score = minimax(board, 0, False)
                board[i, j] = ""  # Undo move
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# ✅ Streamlit UI Setup
st.title("🎮 Tic-Tac-Toe AI Game")
st.write("Play against AI or with a friend!")

# ✅ Initialize board and turn in session state
if "board" not in st.session_state:
    st.session_state.board = initialize_board()
if "turn" not in st.session_state:
    st.session_state.turn = "X"

# ✅ Display the 3x3 board using Streamlit buttons
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            # Show X, O, or empty space as button
            if st.button(st.session_state.board[i, j] if st.session_state.board[i, j] else " ", key=f"{i}-{j}"):
                # Only allow move if the cell is empty and there's no winner
                if st.session_state.board[i, j] == "" and check_winner(st.session_state.board) is None:
                    st.session_state.board[i, j] = st.session_state.turn
                    # Switch turn
                    st.session_state.turn = "O" if st.session_state.turn == "X" else "X"

# ✅ If it's AI's turn and game is not over, let AI play
if st.session_state.turn == "O" and check_winner(st.session_state.board) is None:
    move = best_move(st.session_state.board)
    if move:
        st.session_state.board[move] = "O"
        st.session_state.turn = "X"

# ✅ Display result after every move
winner = check_winner(st.session_state.board)
if winner:
    if winner != "Draw":
        st.success(f"🎉 Winner: {winner}!")
    else:
        st.warning("It's a Draw!")

    # ✅ Button to restart game
    if st.button("Restart Game"):
        st.session_state.board = initialize_board()
        st.session_state.turn = "X"

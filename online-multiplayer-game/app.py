import streamlit as st
import time
import uuid
from datetime import datetime

# Initialize session state variables if they don't exist
if 'game_id' not in st.session_state:
    st.session_state.game_id = ""
if 'player_id' not in st.session_state:
    st.session_state.player_id = str(uuid.uuid4())
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""
if 'game_state' not in st.session_state:
    st.session_state.game_state = None

# Set up the page config
st.set_page_config(page_title="Multiplayer Tic-Tac-Toe", page_icon="🎮", layout="centered")
st.title("Multiplayer Tic-Tac-Toe")

# Function to create a new game
def create_new_game():
    game_id = str(uuid.uuid4())[:8]
    st.session_state.game_id = game_id
    
    # Initialize game state in the session state
    game_state = {
        "board": [" " for _ in range(9)],
        "current_turn": "X",
        "players": {
            "X": {"id": st.session_state.player_id, "name": st.session_state.player_name},
            "O": {"id": None, "name": None}
        },
        "winner": None,
        "last_updated": datetime.now().isoformat(),
        "moves": []
    }
    
    # Save to "database" (using Streamlit's experimental_memo as a simple database)
    st.session_state[f"game_{game_id}"] = game_state
    st.session_state.game_state = game_state
    return game_id

# Function to join an existing game
def join_game(game_id):
    if f"game_{game_id}" not in st.session_state:
        st.error("Game not found!")
        return False
    
    game_state = st.session_state[f"game_{game_id}"]
    
    # Check if can join as player O
    if game_state["players"]["O"]["id"] is None:
        game_state["players"]["O"]["id"] = st.session_state.player_id
        game_state["players"]["O"]["name"] = st.session_state.player_name
        game_state["last_updated"] = datetime.now().isoformat()
        st.session_state[f"game_{game_id}"] = game_state
    elif game_state["players"]["X"]["id"] == st.session_state.player_id or game_state["players"]["O"]["id"] == st.session_state.player_id:
        # Player is already in the game
        pass
    else:
        st.error("Game is full!")
        return False
    
    st.session_state.game_id = game_id
    st.session_state.game_state = game_state
    return True

# Function to make a move
def make_move(position):
    game_id = st.session_state.game_id
    game_state = st.session_state[f"game_{game_id}"]
    
    # Determine player symbol
    player_symbol = None
    if game_state["players"]["X"]["id"] == st.session_state.player_id:
        player_symbol = "X"
    elif game_state["players"]["O"]["id"] == st.session_state.player_id:
        player_symbol = "O"
    
    # Check if it's the player's turn and the position is empty
    if (player_symbol == game_state["current_turn"] and 
        game_state["board"][position] == " " and
        game_state["winner"] is None):
        
        # Make the move
        game_state["board"][position] = player_symbol
        game_state["moves"].append({"position": position, "player": player_symbol})
        
        # Check for winner
        game_state["winner"] = check_winner(game_state["board"])
        
        # Switch turns
        game_state["current_turn"] = "O" if player_symbol == "X" else "X"
        
        # Update timestamp
        game_state["last_updated"] = datetime.now().isoformat()
        
        # Update game state in "database"
        st.session_state[f"game_{game_id}"] = game_state
        st.session_state.game_state = game_state

# Function to check for a winner
def check_winner(board):
    # Define winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in winning_combinations:
        if (board[combo[0]] != " " and
            board[combo[0]] == board[combo[1]] == board[combo[2]]):
            return board[combo[0]]
    
    # Check for a tie
    if " " not in board:
        return "Tie"
    
    return None

# Function to refresh game state
def refresh_game_state():
    if st.session_state.game_id:
        game_id = st.session_state.game_id
        if f"game_{game_id}" in st.session_state:
            st.session_state.game_state = st.session_state[f"game_{game_id}"]

# Function to reset the game
def reset_game():
    game_id = st.session_state.game_id
    game_state = st.session_state[f"game_{game_id}"]
    
    # Reset board
    game_state["board"] = [" " for _ in range(9)]
    game_state["current_turn"] = "X"
    game_state["winner"] = None
    game_state["moves"] = []
    game_state["last_updated"] = datetime.now().isoformat()
    
    # Update game state
    st.session_state[f"game_{game_id}"] = game_state
    st.session_state.game_state = game_state

# Game lobby section
st.subheader("Game Lobby")

# Player name input
player_name = st.text_input("Your Name:", key="name_input")
if player_name:
    st.session_state.player_name = player_name

# Create or join game options
col1, col2 = st.columns(2)

with col1:
    if st.button("Create New Game"):
        if st.session_state.player_name:
            game_id = create_new_game()
            st.success(f"Game created! Game ID: {game_id}")
            st.info("Share this ID with your friend to join.")
        else:
            st.error("Please enter your name first.")

with col2:
    join_id = st.text_input("Join Game (Enter Game ID):")
    if st.button("Join Game"):
        if st.session_state.player_name and join_id:
            if join_game(join_id):
                st.success(f"Joined game {join_id} successfully!")
        elif not st.session_state.player_name:
            st.error("Please enter your name first.")
        else:
            st.error("Please enter a Game ID.")

st.divider()

# Game board display
if st.session_state.game_id and st.session_state.game_state:
    # Auto-refresh game state (checking every 2 seconds)
    refresh_game_state()
    
    # Show game info
    st.subheader(f"Game ID: {st.session_state.game_id}")
    
    game_state = st.session_state.game_state
    
    # Display player information
    st.write(f"Player X: {game_state['players']['X']['name'] or 'Waiting...'}")
    st.write(f"Player O: {game_state['players']['O']['name'] or 'Waiting...'}")
    
    # Display whose turn it is
    if game_state["winner"] is None:
        if game_state["players"]["O"]["id"] is None:
            st.info("Waiting for player O to join...")
        else:
            st.info(f"Current turn: {game_state['current_turn']} ({game_state['players'][game_state['current_turn']]['name']})")
    
    # Display winner message
    if game_state["winner"] == "Tie":
        st.success("Game ended in a tie!")
    elif game_state["winner"]:
        st.success(f"Player {game_state['winner']} ({game_state['players'][game_state['winner']]['name']}) wins!")
    
    # Display game board
    board = game_state["board"]
    
    # Create 3x3 grid for the board
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            pos = i + j
            with cols[j]:
                if board[pos] == " ":
                    if st.button("⠀", key=f"pos_{pos}", use_container_width=True, 
                                 disabled=game_state["winner"] is not None or 
                                          not (game_state["players"]["X"]["id"] == st.session_state.player_id and game_state["current_turn"] == "X") and
                                          not (game_state["players"]["O"]["id"] == st.session_state.player_id and game_state["current_turn"] == "O")):
                        make_move(pos)
                        st.rerun()
                else:
                    st.button(board[pos], key=f"pos_{pos}", use_container_width=True, disabled=True)
    
    # Reset game button
    if game_state["winner"] is not None:
        if st.button("Reset Game"):
            reset_game()
            st.rerun()
    
    # Auto-refresh every 2 seconds
    time.sleep(2)
    st.rerun()

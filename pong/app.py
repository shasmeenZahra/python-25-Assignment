import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw

# Game Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 120
PADDLE_SPEED = 20
BALL_SPEED = 5

def create_game_frame(ball_pos, paddle1_pos, paddle2_pos):
    """Create a frame of the game as a PIL Image"""
    image = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw center line
    for y in range(0, HEIGHT, 20):
        draw.line([(WIDTH//2, y), (WIDTH//2, y+10)], fill=(255, 255, 255), width=2)
    
    # Draw paddles
    draw.rectangle([10, paddle1_pos, 10+PADDLE_WIDTH, paddle1_pos+PADDLE_HEIGHT], 
                  fill=(255, 255, 255))
    draw.rectangle([WIDTH-20, paddle2_pos, WIDTH-20+PADDLE_WIDTH, paddle2_pos+PADDLE_HEIGHT], 
                  fill=(255, 255, 255))
    
    # Draw ball
    draw.ellipse([ball_pos[0]-BALL_RADIUS, ball_pos[1]-BALL_RADIUS, 
                 ball_pos[0]+BALL_RADIUS, ball_pos[1]+BALL_RADIUS], 
                 fill=(255, 255, 255))
    
    return image

def initialize_game():
    """Initialize game state"""
    if 'ball_pos' not in st.session_state:
        st.session_state.ball_pos = [WIDTH//2, HEIGHT//2]
        st.session_state.ball_dx = BALL_SPEED
        st.session_state.ball_dy = BALL_SPEED
        st.session_state.paddle1_pos = HEIGHT//2 - PADDLE_HEIGHT//2
        st.session_state.paddle2_pos = HEIGHT//2 - PADDLE_HEIGHT//2
        st.session_state.score1 = 0
        st.session_state.score2 = 0
        st.session_state.game_active = False

def update_game_state():
    """Update the game state for one frame"""
    if not st.session_state.game_active:
        return
    
    # Update ball position
    st.session_state.ball_pos[0] += st.session_state.ball_dx
    st.session_state.ball_pos[1] += st.session_state.ball_dy
    
    # Ball collision with top/bottom walls
    if st.session_state.ball_pos[1] <= BALL_RADIUS or st.session_state.ball_pos[1] >= HEIGHT - BALL_RADIUS:
        st.session_state.ball_dy *= -1
    
    # Ball collision with paddles
    paddle1_rect = [10, st.session_state.paddle1_pos, 10+PADDLE_WIDTH, st.session_state.paddle1_pos+PADDLE_HEIGHT]
    paddle2_rect = [WIDTH-20, st.session_state.paddle2_pos, WIDTH-20+PADDLE_WIDTH, st.session_state.paddle2_pos+PADDLE_HEIGHT]
    
    if (st.session_state.ball_pos[0] - BALL_RADIUS <= paddle1_rect[2] and 
        st.session_state.ball_pos[0] + BALL_RADIUS >= paddle1_rect[0] and
        st.session_state.ball_pos[1] + BALL_RADIUS >= paddle1_rect[1] and
        st.session_state.ball_pos[1] - BALL_RADIUS <= paddle1_rect[3]):
        st.session_state.ball_dx *= -1
        st.session_state.ball_pos[0] = paddle1_rect[2] + BALL_RADIUS
    
    if (st.session_state.ball_pos[0] + BALL_RADIUS >= paddle2_rect[0] and 
        st.session_state.ball_pos[0] - BALL_RADIUS <= paddle2_rect[2] and
        st.session_state.ball_pos[1] + BALL_RADIUS >= paddle2_rect[1] and
        st.session_state.ball_pos[1] - BALL_RADIUS <= paddle2_rect[3]):
        st.session_state.ball_dx *= -1
        st.session_state.ball_pos[0] = paddle2_rect[0] - BALL_RADIUS
    
    # Ball out of bounds
    if st.session_state.ball_pos[0] < 0:
        st.session_state.score2 += 1
        st.session_state.ball_pos = [WIDTH//2, HEIGHT//2]
        st.session_state.ball_dx = BALL_SPEED
        st.session_state.ball_dy = BALL_SPEED
    elif st.session_state.ball_pos[0] > WIDTH:
        st.session_state.score1 += 1
        st.session_state.ball_pos = [WIDTH//2, HEIGHT//2]
        st.session_state.ball_dx = -BALL_SPEED
        st.session_state.ball_dy = BALL_SPEED

# Main Streamlit App
st.title("Pong Game")
st.write("Use W/S for Player 1 and Up/Down for Player 2")

# Initialize game state
initialize_game()

# Keyboard Input
keys = st.text_input("Press W/S for Player 1, Up/Down for Player 2:")
if "w" in keys:
    st.session_state.paddle1_pos = max(0, st.session_state.paddle1_pos - PADDLE_SPEED)
if "s" in keys:
    st.session_state.paddle1_pos = min(HEIGHT - PADDLE_HEIGHT, st.session_state.paddle1_pos + PADDLE_SPEED)
if "UP" in keys:
    st.session_state.paddle2_pos = max(0, st.session_state.paddle2_pos - PADDLE_SPEED)
if "DOWN" in keys:
    st.session_state.paddle2_pos = min(HEIGHT - PADDLE_HEIGHT, st.session_state.paddle2_pos + PADDLE_SPEED)

# Start and Reset Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start/Pause"):
        st.session_state.game_active = not st.session_state.game_active
with col2:
    if st.button("Reset"):
        initialize_game()

# Display score
st.write(f"Score: Player 1: {st.session_state.score1} - Player 2: {st.session_state.score2}")

# Update game state and display game frame
update_game_state()
game_image = create_game_frame(
    st.session_state.ball_pos,
    st.session_state.paddle1_pos,
    st.session_state.paddle2_pos
)
st.image(game_image, use_container_width=True)

# Auto-refresh for continuous game update
if st.session_state.game_active:
    time.sleep(0.1)
    st.rerun()

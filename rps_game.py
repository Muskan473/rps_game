import streamlit as st
import random

st.set_page_config(page_title="Rock Paper Scissors", layout="centered")

st.title("Rock Paper Scissors Game")
st.subheader("Can you beat an AI that learns from you?")

choices = ["rock", "paper", "scissors"]
emoji_map = {
    "rock": "✊",
    "paper": "✋",
    "scissors": "✌️"
}

if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "user_history" not in st.session_state:
    st.session_state.user_history = []

# AI prediction based on user history
def predict_user_move():
    if not st.session_state.user_history:
        return random.choice(choices)
    
    move_counts = {move: st.session_state.user_history.count(move) for move in choices}
    predicted_move = max(move_counts, key=move_counts.get)

    counter_moves = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }
    return counter_moves[predicted_move]

# Game logic
def play(user_choice): 
    st.session_state.user_history.append(user_choice)
    ai_choice = predict_user_move()

    if user_choice == ai_choice:
        result = f"It's a tie! You both chose {emoji_map[user_choice]}"
    elif (
        (user_choice == "rock" and ai_choice == "scissors") or 
        (user_choice == "paper" and ai_choice == "rock") or 
        (user_choice == "scissors" and ai_choice == "paper")
    ):
        st.session_state.user_score += 1
        result = f"You win! {emoji_map[user_choice]} beats {emoji_map[ai_choice]}"
    else:
        st.session_state.ai_score += 1
        result = f"AI wins! {emoji_map[ai_choice]} beats {emoji_map[user_choice]}"
    
    st.session_state.last_result = result

# Buttons for player choice
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✊ Rock"):
        play("rock")
with col2:
    if st.button("✋ Paper"):
        play("paper")
with col3:
    if st.button("✌️ Scissors"):
        play("scissors")

# Show result
if st.session_state.last_result:
    st.markdown(f"### {st.session_state.last_result}")

# Scoreboard
st.markdown("---")
st.markdown(f"**You:** {st.session_state.user_score} &nbsp;&nbsp;&nbsp;&nbsp; **AI:** {st.session_state.ai_score}")

# Reset button
if st.button("🔁 Reset Game"):
    st.session_state.user_score = 0
    st.session_state.ai_score = 0
    st.session_state.last_result = ""
    st.session_state.user_history = []

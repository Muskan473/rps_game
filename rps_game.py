import streamlit as st
import random

st.set_page_config(page_title="Rock Paper Scissors AI", layout="centered")

# Title
st.markdown("<h1 style='text-align:center; color:#4A90E2;'>✊✋✌️ Rock Paper Scissors AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Can you outsmart an AI that learns your strategy?</p>", unsafe_allow_html=True)

# Game setup
choices = ["rock", "paper", "scissors"]
emoji_map = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
color_map = {"win": "green", "lose": "red", "tie": "gray"}

# Session state
for key, val in {
    "user_score": 0,
    "ai_score": 0,
    "last_result": "",
    "user_history": [],
    "rounds": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# AI Prediction Logic
def predict_user_move():
    if not st.session_state.user_history:
        return random.choice(choices)
    
    move_counts = {move: st.session_state.user_history.count(move) for move in choices}
    predicted_move = max(move_counts, key=move_counts.get)
    counter_moves = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return counter_moves[predicted_move], predicted_move


# Game Logic
def play(user_choice):
    st.session_state.user_history.append(user_choice)
    ai_choice, predicted = predict_user_move()
    st.session_state.rounds += 1

    # Determine result
    if user_choice == ai_choice:
        outcome = "tie"
        result = f"It's a tie! You both chose {emoji_map[user_choice]}"
    elif (
        (user_choice == "rock" and ai_choice == "scissors") or 
        (user_choice == "paper" and ai_choice == "rock") or 
        (user_choice == "scissors" and ai_choice == "paper")
    ):
        st.session_state.user_score += 1
        outcome = "win"
        result = f"🎉 You win! {emoji_map[user_choice]} beats {emoji_map[ai_choice]}"
    else:
        st.session_state.ai_score += 1
        outcome = "lose"
        result = f"😈 AI wins! {emoji_map[ai_choice]} beats {emoji_map[user_choice]}"
    
    st.session_state.last_result = (result, outcome, predicted)


# Layout - Buttons
st.markdown("---")
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

# Results
if st.session_state.last_result:
    result_msg, outcome, predicted_move = st.session_state.last_result
    st.markdown(f"<h3 style='color:{color_map[outcome]}; text-align:center'>{result_msg}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center'>🤖 AI predicted you'd choose <b>{predicted_move}</b></p>", unsafe_allow_html=True)

# Stats
st.markdown("---")
user = st.session_state.user_score
ai = st.session_state.ai_score
total = st.session_state.rounds
tie = total - (user + ai)
win_rate = (user / total * 100) if total else 0

st.markdown(f"""
<div style='text-align:center'>
    <h4>📊 Scoreboard</h4>
    <p><b>You:</b> {user} | <b>AI:</b> {ai} | <b>Ties:</b> {tie}</p>
    <p><b>Rounds Played:</b> {total}</p>
    <p><b>Win Rate:</b> {win_rate:.1f}%</p>
</div>
""", unsafe_allow_html=True)

# Reset
st.markdown("---")
if st.button("🔁 Reset Game"):
    for key in ["user_score", "ai_score", "last_result", "user_history", "rounds"]:
        st.session_state[key] = 0 if key != "user_history" and key != "last_result" else ([] if key == "user_history" else "")
    st.success("Game Reset!")

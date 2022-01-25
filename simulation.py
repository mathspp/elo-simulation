import streamlit as st

from player import Question, AlwaysRight


st.title("ELO-based rating system for quizzes")

with st.expander("Rating settings:"):
    st.text("Define the initial ratings for questions and players.")
    INITIAL_Q_RATING = st.slider(
        "Initial question rating:", min_value=100, max_value=2000, value=1000
    )
    INITIAL_PLAYER_RATING = st.slider(
        "Initial player rating:", min_value=100, max_value=2000, value=1000
    )

QUESTIONS = st.slider("Number of questions:", min_value=10, max_value=100, value=20)
PLAYERS = st.slider("Number of players:", min_value=100, max_value=10_000, value=300)

players = [AlwaysRight(INITIAL_PLAYER_RATING) for _ in range(PLAYERS)]
questions = [Question(INITIAL_Q_RATING) for _ in range(QUESTIONS)]

plot = st.line_chart([])

for q in questions:
    for p in players:
        p.answer_and_update(q)
    plot.add_rows([q.rating])

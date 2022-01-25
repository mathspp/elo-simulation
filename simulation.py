import random

import streamlit as st

from player import Question, UsuallyRight


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

questions = [Question(INITIAL_Q_RATING) for _ in range(QUESTIONS)]
players = []
for _ in range(PLAYERS):
    random.shuffle(questions)
    players.append(UsuallyRight(INITIAL_PLAYER_RATING, questions[::]))
all_players = players[::]

plot = st.line_chart(
    {
        "Min question ELO": [],
        "Max question ELO": [],
        "Min player ELO": [],
        "Max player ELO": [],
    }
)

c = 0
while players:
    idx = random.randint(0, len(players) - 1)
    players[idx].answer_next()
    if not players[idx].question_queue:
        players.pop(idx)
    c = (c + 1) % PLAYERS
    if not c:
        plot.add_rows(
            {
                "Min question ELO": [min(q.rating for q in questions)],
                "Max question ELO": [max(q.rating for q in questions)],
                "Min player ELO": [min(p.rating for p in all_players)],
                "Max player ELO": [max(p.rating for p in all_players)],
            }
        )

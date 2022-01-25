import random

import streamlit as st

from player import (
    Question,
    AlwaysRight,
    AlwaysMid,
    AlwaysWrong,
    UsuallyRight,
    UsuallyWrong,
)


PLAYER_COUNT_TEMPLATE = "Total players: {:>4}"
# Archetypes:
PLAYER_ARCHETYPES = [AlwaysRight, AlwaysMid, AlwaysWrong, UsuallyRight, UsuallyWrong]
# Default values:
PLAYER_DEFAULTS = [100, 100, 100, 1000, 1000]


def set_ratings_expander():
    """Set the expander that controls initial player/question ratings."""
    with st.expander("Rating settings"):
        st.text("Define the initial ratings for questions and players.")
        st.session_state["q_rating"] = st.slider(
            "Initial question rating:", min_value=100, max_value=2000, value=1000
        )
        st.session_state["p_rating"] = st.slider(
            "Initial player rating:", min_value=100, max_value=2000, value=1000
        )


def set_player_defaults():
    """Set player sliders to the default values."""

    for cls, default in zip(PLAYER_ARCHETYPES, PLAYER_DEFAULTS):
        st.session_state[cls.__name__ + "value"] = default
        st.session_state[cls.__name__] = default


def set_knowledgeable_players():
    """Set player sliders to a scenario where everyone knows a lot."""

    values = [250, 50, 0, 2000, 0]
    for cls, value in zip(PLAYER_ARCHETYPES, values):
        st.session_state[cls.__name__ + "value"] = value
        st.session_state[cls.__name__] = value


def set_unknowledgeable_players():
    """Set player sliders to a scenario where everyone knows little."""

    values = [0, 50, 250, 0, 2000]
    for cls, value in zip(PLAYER_ARCHETYPES, values):
        st.session_state[cls.__name__ + "value"] = value
        st.session_state[cls.__name__] = value


def set_player_archetype_expander():
    """Set up the expander that contains sliders for the numbers of players."""

    player_count_label = st.text(PLAYER_COUNT_TEMPLATE.format("??"))
    with st.expander("Player archetypes"):
        for cls, default in zip(PLAYER_ARCHETYPES, PLAYER_DEFAULTS):
            st.session_state[cls.__name__ + "value"] = st.slider(
                cls.__name__,
                key=cls.__name__,
                min_value=0,
                max_value=10_000,
                value=st.session_state.get(cls.__name__, default),
            )
        player_count_label.write(
            PLAYER_COUNT_TEMPLATE.format(
                sum(
                    st.session_state[cls.__name__ + "value"]
                    for cls in PLAYER_ARCHETYPES
                )
            )
        )
        col1, col2, col3 = st.columns(3)
        col1.button("Defaults", on_click=set_player_defaults)
        col2.button("Knowledgeables", on_click=set_knowledgeable_players)
        col3.button("Unknowledgeables", on_click=set_unknowledgeable_players)


def run_simulation():
    """Run the simulation with the parameters defined by the Streamlit app."""

    questions = [
        Question(st.session_state["q_rating"])
        for _ in range(st.session_state["questions"])
    ]

    players = []
    for cls in PLAYER_ARCHETYPES:
        for _ in range(st.session_state[cls.__name__ + "value"]):
            random.shuffle(questions)
            players.append(cls(st.session_state["p_rating"], questions[::]))
    all_players = players[::]

    plot = st.line_chart()

    c = 0
    while players:
        idx = random.randint(0, len(players) - 1)
        players[idx].answer_next()
        if not players[idx].question_queue:
            players.pop(idx)

        if not c:
            plot.add_rows(
                {
                    "Min question ELO": [min(q.rating for q in questions)],
                    "Max question ELO": [max(q.rating for q in questions)],
                    "Min player ELO": [min(p.rating for p in all_players)],
                    "Max player ELO": [max(p.rating for p in all_players)],
                }
            )
        c = (c + 1) % len(all_players)


def main():
    """Run the Streamlit app."""

    st.title("ELO-based rating system for quizzes simulation")
    set_ratings_expander()
    st.session_state["questions"] = st.slider(
        "Number of questions:", min_value=10, max_value=100, value=20
    )
    set_player_archetype_expander()
    run_simulation()


if __name__ == "__main__":
    main()

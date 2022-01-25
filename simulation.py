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


def set_questions_sliders():
    st.session_state["questions"] = st.slider(
        "Number of questions:", min_value=10, max_value=100, value=20
    )
    min_current, max_current = st.session_state.get("questions_n", [1, 100])
    max_current = min(max_current, st.session_state["questions"])
    min_current = min(min_current, st.session_state["questions"])
    st.session_state["questions_n"] = st.slider(
        "Players answer a random number of questions between:",
        min_value=1,
        max_value=100,
        value=(min_current, max_current),
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


def set_plot():
    st.subheader("Player and question ELO rating evolution")
    st.session_state["plot"] = st.line_chart()


def run_simulation():
    """Run the simulation with the parameters defined by the Streamlit app."""

    questions = [
        Question(st.session_state["q_rating"])
        for _ in range(st.session_state["questions"])
    ]

    players = []
    total_questions = 0
    for cls in PLAYER_ARCHETYPES:
        for _ in range(st.session_state[cls.__name__ + "value"]):
            random.shuffle(questions)
            min_q, max_q = st.session_state["questions_n"]
            # Pick a random number of questions, from the min, to the maximum allowed.
            to_answer = random.randint(min_q, min(max_q, len(questions)))
            players.append(cls(st.session_state["p_rating"], questions[:to_answer]))
            total_questions += to_answer
    all_players = players[::]

    c = 0
    while players:
        idx = random.randint(0, len(players) - 1)
        players[idx].answer_next()
        if not players[idx].question_queue:
            players.pop(idx)

        if not c:
            st.session_state["plot"].add_rows(
                {
                    "Min question ELO": [min(q.rating for q in questions)],
                    "Max question ELO": [max(q.rating for q in questions)],
                    "Min player ELO": [min(p.rating for p in all_players)],
                    "Max player ELO": [max(p.rating for p in all_players)],
                }
            )
        c = (c + 1) % (total_questions // len(questions))


def main():
    """Run the Streamlit app."""

    st.title("ELO-based rating system for quizzes simulation")
    st.subheader("Accompanying blog article")
    st.markdown(
        "Read the accompanying blog article [here]"
        + "(https://mathspp.com/blog/elo-rating-system-simulation)."
    )

    st.subheader("Simulation parameters")
    set_ratings_expander()
    set_questions_sliders()
    set_player_archetype_expander()
    set_plot()
    run_simulation()


if __name__ == "__main__":
    main()

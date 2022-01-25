from __future__ import annotations

from abc import ABC, abstractmethod
from random import uniform


SCALE_FACTOR = 400
INITIAL_PLAYER_K = 32
FINAL_PLAYER_K = 16
INITIAL_QUESTION_K = 32
FINAL_QUESTION_K = 8


class RatedEntity:
    """Represents an entity that has an ELO-like numerical rating."""

    def __init__(self, rating: float, K: int):
        self.rating = rating
        self.K = K

    def expected_score(self, other: RatedEntity) -> float:
        """Compute the expected score when facing the other rated entity."""
        return 1 / (1 + pow(10, (other.rating - self.rating) / SCALE_FACTOR))

    def update_score(self, expected: float, actual: float):
        """Update the rating according to the given scores."""
        self.rating += self.score_delta(expected, actual)

    def score_delta(self, expected: float, actual: float) -> float:
        """Compute how much the rating would change according to the given scores."""
        return self.K * (actual - expected)


class Question(RatedEntity):
    """Represents a question with an ELO rating.

    A question is a rated entity that defines a strategy to handle the evolution
    of the K factor.
    """

    def __init__(self, rating: float):
        super().__init__(rating, INITIAL_QUESTION_K)

    def update_K(self):
        """Define the strategy to evolve K over time."""
        self.K = max(FINAL_QUESTION_K, self.K - 1)

    def update_score(self, expected: float, actual: float):
        """Update the score of the rated entity and then update K."""
        super().update_score(expected, actual)
        self.update_K()


class Player(RatedEntity, ABC):
    """Represents a player with an ELO rating.

    A player is a rated entity that provides a (possibly random) function
    that determines the score the player would get when answering a question.
    This class also defines a strategy to handle the evolution of the K factor.
    """

    def __init__(self, rating: float):
        super().__init__(rating, INITIAL_PLAYER_K)

    @abstractmethod
    def generate_score(self) -> float:
        """Generates the answering score of the player following its archetype."""
        pass

    def update_K(self):
        """Define the strategy to evolve K over time."""
        self.K = max(FINAL_PLAYER_K, self.K - 1)

    def answer_and_update(self, question: RatedEntity):
        """Answer a question and update own and question's ratings."""
        expected_score = self.expected_score(question)
        actual_score = self.generate_score()
        self.update_score(expected_score, actual_score)
        question.update_score(1 - expected_score, 1 - actual_score)
        self.update_K()


class AlwaysRight(Player):
    """A player that gets all questions correctly."""

    def generate_score(self) -> float:
        return 1


class AlwaysMid(Player):
    """A player that always gets all questions half-right."""

    def generate_score(self) -> float:
        return 0.5


class AlwaysWrong(Player):
    """A player that gets all questions incorrectly."""

    def generate_score(self) -> float:
        return 0


class UsuallyRight(Player):
    """A player with a uniformly distributed score in [0.3, 1]."""

    def generate_score(self) -> float:
        return uniform(0.3, 1)


class UsuallyWrong(Player):
    """A player with a uniformly distributed score in [0, 0.7]."""

    def generate_score(self) -> float:
        return uniform(0, 0.7)


if __name__ == "__main__":
    # Wikipedia examples.
    A = RatedEntity(1613, 32)
    print(A.expected_score(RatedEntity(1609, 32)))  # Should give approximately .51
    print(A.score_delta(2.88, 2.5))  # Should give approximately -12.

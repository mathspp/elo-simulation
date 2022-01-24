from __future__ import annotations


SCALE_FACTOR = 400


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


if __name__ == "__main__":
    # Wikipedia examples.
    A = RatedEntity(1613, 32)
    print(A.expected_score(RatedEntity(1609, 32)))  # Should give approximately .51
    print(A.score_delta(2.88, 2.5))  # Should give approximately -12.

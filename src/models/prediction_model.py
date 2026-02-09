"""
Model describing a single predicted tag from the predictor.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TagPrediction:
    """
    * Attributes:
        - tag_name: Name of the predicted tag.

        - probability: Confidence for the tag in the range [0.0, 1.0].
    """

    tag_name: str
    probability: float

    def __post_init__(self) -> None:
        # Validate numeric range
        if not (0 <= self.probability <= 1):
            raise ValueError(
                f"probability ({self.probability}) must be between 0 and 1 inclusive."
            )

    def __lt__(self, other: TagPrediction) -> bool:
        return self.probability < other.probability

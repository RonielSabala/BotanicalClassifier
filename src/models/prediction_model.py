from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class TagPrediction(BaseModel):
    """
    Model describing a single predicted tag from the predictor.

    * Attributes:
        - tag_name: Name of the predicted tag.

        - probability: Confidence for the tag in [0.0, 1.0].
    """

    tag_name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    probability: float = Field(..., ge=0.0, le=1.0)

    model_config = {"frozen": True, "from_attributes": True}

    def __lt__(self, other: TagPrediction) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.probability < other.probability

from dataclasses import dataclass


@dataclass(slots=True)
class Prediction:
    tag_name: str
    probability: float

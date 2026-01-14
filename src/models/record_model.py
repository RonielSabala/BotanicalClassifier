from dataclasses import dataclass
from typing import Optional

from .prediction_model import Prediction


@dataclass(slots=True)
class Record:
    name: str
    surname: str
    address: str
    image_path: str
    predictions: Optional[list[Prediction]] = None

    @staticmethod
    def from_str(record_str: str) -> "Record":
        return eval(record_str)

    def get_property_by_index(self, index: int) -> str:
        if index == 0:
            return self.name
        if index == 1:
            return self.surname
        if index == 2:
            return self.address

        raise ValueError(f"index ({index}) is not a valid to get the record property.")

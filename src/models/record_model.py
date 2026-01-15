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
    record_id: int = -1

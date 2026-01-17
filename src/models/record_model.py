"""
Model representing a saved survey record.
"""

from dataclasses import dataclass
from typing import Optional

from .prediction_model import TagPrediction


@dataclass(slots=True)
class Record:
    """
    A survey record.

    * Attributes:
        - name, surname, address: Person identification fields.

        - image_path: Filesystem path to the image associated
        with this record.

        - predictions: List of TagPrediction objects, None when
        not yet predicted.

        - record_id: Integer identifier for the record; -1
        indicates unset.
    """

    name: str
    surname: str
    address: str
    image_path: str
    predictions: Optional[list[TagPrediction]] = None
    record_id: int = -1

"""
Service that loads, saves and manages Record objects persisted
as JSON plus image files.
"""

import json
from collections.abc import Iterator
from typing import Any, Optional

from common.paths import LOCAL_IMAGES_DIR, LOCAL_RECORDS_FILE
from models.prediction_model import TagPrediction
from models.record_model import Record

from .predictor_service import PredictorService

type JsonData = dict[str, Any]


class RecordsService:
    @staticmethod
    def _read_records_data() -> JsonData:
        """
        Read and return the parsed JSON content of the
        records file.
        """

        if LOCAL_RECORDS_FILE.stat().st_size == 0:
            # Empty json
            return dict()

        with open(LOCAL_RECORDS_FILE, "r") as f:
            return json.load(f)

    @classmethod
    def next_record_id(cls) -> int:
        """
        Return the next record id.
        """

        return len(tuple(LOCAL_IMAGES_DIR.iterdir()))

    @staticmethod
    def _load_record(record_id: int, data: JsonData) -> Record:
        """
        Reconstruct a Record object for a given `record_id`
        using the provided data mapping.
        """

        key = str(record_id)
        record_data = data.get(key)
        if record_data is None:
            raise ValueError(f"No record with record_id={record_id} exists in storage.")

        # Reconstruct Prediction objects if they exist
        predictions = record_data.get("predictions")
        if predictions:
            record_data["predictions"] = [TagPrediction(**p) for p in predictions]

        return Record(**record_data)

    @classmethod
    def iter_records(cls) -> Iterator[Record]:
        """
        Iterate over all stored records in numeric key order
        yielding Record objects.
        """

        data = cls._read_records_data()
        return (
            cls._load_record(record_id, data)
            for record_id in range(cls.next_record_id())
        )

    @staticmethod
    def delete_all_records() -> None:
        """
        Delete all records and image files.
        """

        LOCAL_RECORDS_FILE.write_text("{}")
        for image_path in LOCAL_IMAGES_DIR.iterdir():
            image_path.unlink()

    @classmethod
    def insert_record(cls, record: Record, data: Optional[JsonData] = None) -> None:
        """
        Insert/update a record in the records file.
        """

        if data is None:
            data = cls._read_records_data()

        key = str(record.record_id)
        data[key] = record.model_dump(exclude_none=True)
        with open(LOCAL_RECORDS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def set_record_prediction(cls, record_id: int) -> None:
        """
        Load a record by id, call the predictor service to
        set predictions on the Record, and persist the
        updated Record back to storage.
        """

        data = cls._read_records_data()
        record = cls._load_record(record_id, data)
        PredictorService.set_flower_prediction(record)
        cls.insert_record(record, data)

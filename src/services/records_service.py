import json
from dataclasses import asdict
from typing import Any, Generator, Optional

from common.paths import LOCAL_IMAGES_DIR, LOCAL_RECORDS_PATH
from models.prediction_model import Prediction
from models.record_model import Record

from .predictor_service import PredictorService

RecordsJson = dict[str, Any]


class RecordsService:
    @staticmethod
    def _get_records_json() -> RecordsJson:
        # Empty file
        if LOCAL_RECORDS_PATH.stat().st_size == 0:
            return dict()

        with open(LOCAL_RECORDS_PATH, "r") as f:
            return json.load(f)

    @classmethod
    def get_next_record_id(cls) -> int:
        return len(tuple(LOCAL_IMAGES_DIR.iterdir()))

    @classmethod
    def _load_record(cls, record_id: int, data: RecordsJson) -> Record:
        record_data = data.get(str(record_id))
        if record_data is None:
            raise ValueError(f"No record with record_id={record_id} exists.")

        # Reconstruct Prediction objects if they exist
        predictions = record_data.get("predictions")
        if predictions:
            record_data["predictions"] = [Prediction(**pred) for pred in predictions]

        return Record(**record_data)

    @classmethod
    def load_all_records(cls) -> Generator[Record, None, None]:
        data = cls._get_records_json()
        return (
            cls._load_record(record_id, data)
            for record_id in range(cls.get_next_record_id())
        )

    @staticmethod
    def delete_all_records() -> None:
        """
        Elimina todos los formularios e imágenes.
        """

        # Clean records
        LOCAL_RECORDS_PATH.write_text("{}")

        # Delete images
        for image_file in LOCAL_IMAGES_DIR.iterdir():
            image_file.unlink()

    @classmethod
    def insert_record(cls, record: Record, data: Optional[RecordsJson] = None) -> None:
        if data is None:
            data = cls._get_records_json()

        data[str(record.record_id)] = asdict(record)

        # Update data
        with open(LOCAL_RECORDS_PATH, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def set_record_prediction(cls, record_id: int) -> None:
        """
        Inserta en el registro de la línea especificada
        la clasificación de la imagen que tiene dicho registro.
        """

        data = cls._get_records_json()
        record = cls._load_record(record_id, data)
        PredictorService.set_flower_prediction(record)
        cls.insert_record(record, data)

    @staticmethod
    def get_record_property_by_index(record: Record, index: int) -> str:
        if index == 0:
            return record.name
        if index == 1:
            return record.surname
        if index == 2:
            return record.address

        raise ValueError(f"index ({index}) is not a valid to get the record property.")

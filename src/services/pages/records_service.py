import os

from common.paths import LOCAL_IMAGES_DIR, LOCAL_RECORDS_PATH
from common.utils import get_local_image_path
from models.record_model import Record

from ..predictor_service import get_flower_prediction


class RecordsService:
    @staticmethod
    def get_all_records() -> tuple[Record, ...]:
        with open(LOCAL_RECORDS_PATH, "r") as f:
            return tuple(map(Record.from_str, f.readlines()))

    @staticmethod
    def delete_all_records() -> None:
        """
        Elimina todos los formularios e imágenes.
        """

        # Clean records file
        with open(LOCAL_RECORDS_PATH, "w") as f:
            f.write("")

        # Delete record images
        for image_path in os.listdir(LOCAL_IMAGES_DIR):
            os.unlink(get_local_image_path(image_path))

    @staticmethod
    def set_record_prediction(record_index: int) -> None:
        """
        Inserta en el registro de la línea especificada
        la clasificación de la imagen que tiene dicho registro.
        """

        # Get records
        with open(LOCAL_RECORDS_PATH, "r") as f:
            records_str = f.readlines()

        # Validate record index
        if not (0 <= record_index < len(records_str)):
            raise ValueError(
                f"Error inserting prediction: record_index ({record_index}) out of range."
            )

        # Set prediction
        record = Record.from_str(records_str[record_index])
        record.predictions = get_flower_prediction(record.image_path)

        # Update records
        records_str[record_index] = f"{record}\n"
        with open(LOCAL_RECORDS_PATH, "w") as f:
            f.writelines(records_str)

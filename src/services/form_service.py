import shutil
from pathlib import Path

from common.constants import LOCAL_IMAGES_PREFIX
from common.paths import (
    LOCAL_IMAGES_DIR,
)
from common.utils import is_valid_path, show_error_messagebox
from models.record_model import Record
from services.records_service import RecordsService

from .i18n_service import i18n


class FormService:
    @classmethod
    def save_form(cls, record: Record) -> None:
        """
        Guarda un registro en el archivo formularios.
        """

        # - Update record id and image path:

        record_id = RecordsService.get_next_record_id()
        user_image_path = Path(record.image_path)
        image_extension = user_image_path.suffix.lower()
        image_filename = f"{LOCAL_IMAGES_PREFIX}_{record_id}{image_extension}"
        image_path = str(LOCAL_IMAGES_DIR / image_filename)

        record.record_id = record_id
        record.image_path = image_path

        # Save record and image
        RecordsService.insert_record(record)
        shutil.copy(user_image_path, image_path)

    @staticmethod
    def _validate_entry(entry_name: str, name_on_error: str) -> bool:
        """
        Si el campo es válido devuelve True, de otro
        modo False y muestra un error personalizado.
        """

        is_valid = True
        error_msg = f"{i18n.get('form.utils.enter_entry')} {name_on_error}"
        if not entry_name:
            is_valid = False

        elif len(entry_name) < 5:
            is_valid = False
            error_msg += " " + i18n.get("form.utils.minimum_char_requirement")

        elif len(entry_name) > 50:
            is_valid = False
            error_msg += " " + i18n.get("form.utils.maximum_char_requirement")

        if not is_valid:
            show_error_messagebox(error_msg + ".")

        return is_valid

    @staticmethod
    def _validate_image_path(image_path: str) -> bool:
        error_msg = None
        if image_path == i18n.get("form.utils.attach_image"):
            error_msg = i18n.get("form.utils.unselected_image_error")

        elif not is_valid_path(image_path):
            error_msg = i18n.get("form.utils.invalid_image_error")

        is_valid = error_msg is None
        if not is_valid:
            show_error_messagebox(error_msg)

        return is_valid

    @classmethod
    def validate_record(cls, record: Record) -> bool:
        return (
            cls._validate_entry(record.name, i18n.get("form.utils.enter_name"))
            and cls._validate_entry(
                record.surname, i18n.get("form.utils.enter_surname")
            )
            and cls._validate_entry(
                record.address, i18n.get("form.utils.enter_address")
            )
            and cls._validate_image_path(record.image_path)
        )

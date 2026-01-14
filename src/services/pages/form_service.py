import os
import shutil

from common.constants import LOCAL_IMAGES_PREFIX
from common.paths import (
    LOCAL_IMAGES_DIR,
    LOCAL_RECORDS_PATH,
)
from common.utils import get_local_image_path, is_valid_path, show_error_messagebox
from models.record_model import Record

from ..i18n_service import i18n


class FormService:
    @staticmethod
    def _get_next_image_filename(img_extension: str) -> str:
        images_count = len(os.listdir(LOCAL_IMAGES_DIR))
        return f"{LOCAL_IMAGES_PREFIX}_{images_count}.{img_extension}"

    @classmethod
    def save_record(cls, record: Record) -> None:
        """
        Guarda un registro en el archivo formularios.
        """

        # Get next image filename
        image_path = record.image_path
        image_extension = (image_path.split(".")[-1]).lower()
        image_filename = cls._get_next_image_filename(image_extension)

        # Get local image path
        local_image_path = get_local_image_path(image_filename)
        record.image_path = local_image_path

        # Copy image to the local path
        shutil.copy(image_path, local_image_path)

        # Save record
        with open(LOCAL_RECORDS_PATH, "a") as f:
            f.write(f"{record}\n")

    @staticmethod
    def _validate_entry(entry_name: str, name_on_error: str) -> bool:
        """
        Si el campo es válido devuelve True, de otro
        modo False y muestra un error personalizado.
        """

        is_valid = True
        enter_entry = i18n.get("form.utils.enter_entry")
        error_msg = f"{enter_entry} {name_on_error}"
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
            and FormService._validate_image_path(record.image_path)
        )

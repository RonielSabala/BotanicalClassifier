import os

from common.constants import LOCAL_IMAGES_PREFIX
from common.paths import (
    LOCAL_IMAGES_DIR,
    LOCAL_RECORDS_PATH,
)
from common.utils import is_valid_path, show_error_messagebox

from ..i18n_service import i18n


class FormService:
    @staticmethod
    def get_next_image_filename(img_extension: str) -> str:
        images_count = len(os.listdir(LOCAL_IMAGES_DIR))
        return f"{LOCAL_IMAGES_PREFIX}_{images_count}.{img_extension}"

    @staticmethod
    def append_record(record: str) -> None:
        """
        Guarda un registro en el archivo formularios.
        """

        with open(LOCAL_RECORDS_PATH, "a") as f:
            f.write(f"{record}\n")

    @staticmethod
    def _is_valid_entry(entry_name: str, name_on_error: str) -> bool:
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

    @classmethod
    def is_valid_name(cls, name: str) -> bool:
        return cls._is_valid_entry(name, i18n.get("form.utils.enter_name"))

    @classmethod
    def is_valid_surname(cls, last_name: str) -> bool:
        return cls._is_valid_entry(last_name, i18n.get("form.utils.enter_surname"))

    @classmethod
    def is_valid_address(cls, address: str) -> bool:
        return cls._is_valid_entry(address, i18n.get("form.utils.enter_address"))

    @staticmethod
    def is_valid_image_path(image_path: str) -> bool:
        error_msg = None
        if image_path == i18n.get("form.utils.attach_image"):
            error_msg = i18n.get("form.utils.unselected_image_error")

        elif not is_valid_path(image_path):
            error_msg = i18n.get("form.utils.invalid_image_error")

        is_valid = error_msg is None
        if not is_valid:
            show_error_messagebox(error_msg)

        return is_valid

"""
Service for form-level validations and persistence helpers.
"""

import shutil
from pathlib import Path

from common.constants import IMAGE_FILENAME_PREFIX
from common.paths import (
    LOCAL_IMAGES_DIR,
)
from common.utils import path_exists, show_error_messagebox
from models.record_model import Record
from services.records_service import RecordsService

from .i18n_service import i18n


class FormService:
    @classmethod
    def _get_image_dest(cls, user_image_path: Path, record_id: int) -> Path:
        """
        Return the final image destination using the `flower_survey_xx`
        convention.
        """

        record_id += 1
        flower_number = f"0{record_id}" if record_id < 10 else str(record_id)
        image_extension = user_image_path.suffix.lower()

        # Build path
        image_filename = f"{IMAGE_FILENAME_PREFIX}{flower_number}{image_extension}"
        return LOCAL_IMAGES_DIR / image_filename

    @classmethod
    def save_form(cls, record: Record) -> None:
        """
        Persist the given record and copy the user's image
        into the local images directory.
        """

        # Determine next id
        record_id = RecordsService.next_record_id()

        # Normalize user-provided image path
        user_image_path = Path(record.image_path)
        dest_path = cls._get_image_dest(user_image_path, record_id)

        # Update record
        record.record_id = record_id
        record.image_path = str(dest_path)

        # Save data
        shutil.copy(user_image_path, dest_path)
        RecordsService.insert_record(record)

    @staticmethod
    def _validate_text_entry(entry_value: str, name_on_error: str) -> bool:
        """
        Validate a text entry (name/surname/address). On failure,
        shows a localized error dialog and returns False.
        """

        is_valid = True
        error_msg = f"{i18n.get('form.utils.enter_entry')} {name_on_error}"
        if not entry_value:
            is_valid = False

        elif len(entry_value) < 5:
            is_valid = False
            error_msg += " " + i18n.get("form.utils.minimum_char_requirement")

        elif len(entry_value) > 50:
            is_valid = False
            error_msg += " " + i18n.get("form.utils.maximum_char_requirement")

        if not is_valid:
            show_error_messagebox(error_msg + ".")

        return is_valid

    @staticmethod
    def _validate_image_path(image_path: str) -> bool:
        """
        Validates the user image. If the UI placeholder text is
        still present, treat as unselected, otherwise, check
        filesystem existence.

        On failure, show localized error and return False.
        """

        error_msg = None
        if image_path == i18n.get("form.utils.attach_image"):
            error_msg = i18n.get("form.utils.unselected_image_error")

        elif not path_exists(image_path):
            error_msg = i18n.get("form.utils.invalid_image_error")

        is_valid = error_msg is None
        if not is_valid:
            show_error_messagebox(error_msg)

        return is_valid

    @classmethod
    def validate_record(cls, record: Record) -> bool:
        """
        Validate a given record and returns True if all
        validations pass, False otherwise and shows dialogs.
        """

        return (
            cls._validate_text_entry(record.name, i18n.get("form.utils.enter_name"))
            and cls._validate_text_entry(
                record.surname, i18n.get("form.utils.enter_surname")
            )
            and cls._validate_text_entry(
                record.address, i18n.get("form.utils.enter_address")
            )
            and cls._validate_image_path(record.image_path)
        )


# Public API
__all__ = ("FormService",)

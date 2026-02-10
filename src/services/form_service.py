"""
Service for form-level validations and persistence helpers.
"""

import shutil
from pathlib import Path

from common.constants import IMAGE_FILENAME_PREFIX
from common.paths import LOCAL_IMAGES_DIR
from models.record_model import Record
from services.records_service import RecordsService


class FormService:
    @classmethod
    def _get_image_dest(cls, user_image_path: Path, record_id: int) -> Path:
        """
        Return the final image destination using the `flower_survey_xx`
        convention.
        """

        image_extension = user_image_path.suffix.lower()
        image_file = f"{IMAGE_FILENAME_PREFIX}{(record_id + 1):02d}{image_extension}"
        return LOCAL_IMAGES_DIR / image_file

    @classmethod
    def save_form(cls, record: Record) -> None:
        """
        Persist the given record and copy the user's image
        into the local images directory.
        """

        new_record_id = RecordsService.next_record_id()

        # Normalize user-provided image path
        user_image_path = Path(record.image_path)
        dest_path = cls._get_image_dest(user_image_path, new_record_id)

        # Update record
        record.record_id = new_record_id
        record.image_path = str(dest_path)

        # Save data
        RecordsService.insert_record(record)
        shutil.copy(user_image_path, dest_path)

from typing import Optional

from pydantic import BaseModel, field_validator

from common.utils import path_exists
from services.i18n_service import i18n

from .prediction_model import TagPrediction

_MIN_STR_LEN = 5
_MAX_STR_LEN = 50


class Record(BaseModel):
    """
    A survey record.

    * Attributes:
        - name, surname, address: Person identification fields.

        - image_path: Path string to the image associated with
        this record.

        - predictions: Optional list of TagPrediction objects, None
        when not yet predicted.

        - record_id: Integer identifier; -1 indicates unset.
    """

    name: str
    surname: str
    address: str
    image_path: str
    predictions: Optional[list[TagPrediction]] = None
    record_id: int = -1

    model_config = {"from_attributes": True}

    # - Validators:

    @classmethod
    def _validate_text_entry(cls, value: str, field_name: str) -> str:
        """
        Validate a text entry. On failure, raises `ValueError` with
        localized error message.
        """

        error_msg = i18n.get("form.utils.enter_entry") + " " + field_name

        is_valid = True
        if not value:
            is_valid = False

        elif len(value) < _MIN_STR_LEN:
            is_valid = False
            error_msg += " " + i18n.get("form.utils.minimum_char_requirement")

        elif len(value) > _MAX_STR_LEN:
            is_valid = False
            error_msg += " " + i18n.get("form.utils.maximum_char_requirement")

        if not is_valid:
            raise ValueError(error_msg)

        return value

    @field_validator("name")
    @classmethod
    def _validate_name(cls, name: str, info) -> str:
        return cls._validate_text_entry(name, i18n.get("form.utils.enter_name"))

    @field_validator("surname")
    @classmethod
    def _validate_surname(cls, surname: str, info) -> str:
        return cls._validate_text_entry(surname, i18n.get("form.utils.enter_surname"))

    @field_validator("address")
    @classmethod
    def _validate_address(cls, address: str, info) -> str:
        return cls._validate_text_entry(address, i18n.get("form.utils.enter_address"))

    @field_validator("image_path")
    @classmethod
    def _validate_image_path(cls, value: str) -> str:
        """
        Validates the image path. If the UI placeholder text is
        still present, treat as unselected, otherwise, check
        filesystem existence.

        On failure, raises `ValueError` with localized error
        message.
        """

        placeholder = i18n.get("form.utils.attach_image")
        if value == placeholder:
            raise ValueError(i18n.get("form.utils.unselected_image_error"))

        if not path_exists(value):
            raise ValueError(i18n.get("form.utils.invalid_image_error"))

        return value

    # - Helpers:

    def get_property_by_index(self, index: int) -> str:
        """
        Map `index` to the instance properties (in order).
        Index 0 -> name, 1 -> surname, 2 -> address.
        Raises `IndexError` when `index` is invalid.
        """

        if index == 0:
            return self.name
        if index == 1:
            return self.surname
        if index == 2:
            return self.address

        raise ValueError(f"index ({index}) is not valid for record properties.")

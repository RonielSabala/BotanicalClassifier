"""
Path constants and helper functions for repository resources.
"""

from pathlib import Path
from typing import Final

_SRC_DIR: Final[Path] = Path(__file__).resolve().parent.parent
_RESOURCES_DIR: Final[Path] = _SRC_DIR / "resources"

# Local storage
LOCAL_RESOURCES_DIR: Final[Path] = _RESOURCES_DIR / "local"
LOCAL_IMAGES_DIR: Final[Path] = LOCAL_RESOURCES_DIR / "images"
LOCAL_RECORDS_FILE: Final[Path] = LOCAL_RESOURCES_DIR / "records.json"

# Images
_IMAGES_DIR: Final[Path] = _RESOURCES_DIR / "images"
APP_ICON_IMAGE_PATH: Final[Path] = _IMAGES_DIR / "app_icon.png"
APP_BANNER_IMAGE_PATH: Final[Path] = _IMAGES_DIR / "app_banner.png"
COUNTRY_SHIELD_IMAGE_PATH: Final[Path] = _IMAGES_DIR / "country_shield.png"
EMPTY_IMAGE_PATH: Final[Path] = _IMAGES_DIR / "empty_image.png"


def i18n_file_path(lang: str) -> Path:
    """
    Return the path to the i18n JSON file for the
    given language code.
    """

    return _RESOURCES_DIR / "i18n" / f"{lang}.json"


def _about_content_dir(lang: str) -> Path:
    """
    Return the directory path containing about content
    for the given language code.
    """

    return _RESOURCES_DIR / "content" / lang


def faq_path(lang: str) -> Path:
    """
    Return the FAQ text file path for the given language.
    """

    return _about_content_dir(lang) / "faq.txt"


def terms_path(lang: str) -> Path:
    """
    Return the Terms text file path for the given language.
    """

    return _about_content_dir(lang) / "terms.txt"


def policies_path(lang: str) -> Path:
    """
    Return the Policies text file path for the given language.
    """

    return _about_content_dir(lang) / "policies.txt"


# Public API
__all__ = (
    "LOCAL_RESOURCES_DIR",
    "LOCAL_IMAGES_DIR",
    "LOCAL_RECORDS_FILE",
    "APP_ICON_IMAGE_PATH",
    "APP_BANNER_IMAGE_PATH",
    "COUNTRY_SHIELD_IMAGE_PATH",
    "EMPTY_IMAGE_PATH",
    "i18n_file_path",
    "faq_path",
    "terms_path",
    "policies_path",
)

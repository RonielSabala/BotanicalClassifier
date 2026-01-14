from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent

_RESOURCES_DIR = SRC_DIR / "resources"
I18N_DIR = _RESOURCES_DIR / "i18n"

# Local storage paths
LOCAL_RESOURCES_DIR = _RESOURCES_DIR / "local"
LOCAL_IMAGES_DIR = LOCAL_RESOURCES_DIR / "images"
LOCAL_RECORDS_PATH = LOCAL_RESOURCES_DIR / "records.txt"

# Images paths
_IMAGES_DIR = _RESOURCES_DIR / "images"
APP_ICON_IMAGE_PATH = _IMAGES_DIR / "app_icon.png"
APP_BANNER_IMAGE_PATH = _IMAGES_DIR / "app_banner.png"
COUNTRY_SHIELD_IMAGE_PATH = _IMAGES_DIR / "country_shield.png"
EMPTY_IMAGE_PATH = _IMAGES_DIR / "empty_image.png"

# About content paths
_ABOUT_CONTENT_DIR = _RESOURCES_DIR / "content/{lang}"
FAQ_PATH = _ABOUT_CONTENT_DIR / "faq.txt"
TERMS_PATH = _ABOUT_CONTENT_DIR / "terms.txt"
POLICIES_PATH = _ABOUT_CONTENT_DIR / "policies.txt"

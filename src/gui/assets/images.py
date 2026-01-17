from common.paths import (
    APP_BANNER_IMAGE_PATH,
    APP_ICON_IMAGE_PATH,
    COUNTRY_SHIELD_IMAGE_PATH,
    EMPTY_IMAGE_PATH,
)
from common.utils import load_image_tk, load_resized_image_tk

APP_ICON_IMAGE = load_image_tk(APP_ICON_IMAGE_PATH)
APP_BANNER_IMAGE = load_image_tk(APP_BANNER_IMAGE_PATH)
COUNTRY_SHIELD_IMAGE = load_image_tk(COUNTRY_SHIELD_IMAGE_PATH)
EMPTY_IMAGE = load_resized_image_tk(EMPTY_IMAGE_PATH)

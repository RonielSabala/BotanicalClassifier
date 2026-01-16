from common.paths import (
    APP_BANNER_IMAGE_PATH,
    APP_ICON_IMAGE_PATH,
    COUNTRY_SHIELD_IMAGE_PATH,
    EMPTY_IMAGE_PATH,
)
from common.utils import get_image_from_path, get_resized_image

APP_ICON_IMAGE = get_image_from_path(APP_ICON_IMAGE_PATH)
APP_BANNER_IMAGE = get_image_from_path(APP_BANNER_IMAGE_PATH)
COUNTRY_SHIELD_IMAGE = get_image_from_path(COUNTRY_SHIELD_IMAGE_PATH)
EMPTY_IMAGE = get_resized_image(EMPTY_IMAGE_PATH)

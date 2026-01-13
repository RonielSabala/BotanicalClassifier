from PIL import Image, ImageTk

from common.constants import BASE_IMAGE_COLOR, BASE_IMAGE_MODE, BASE_IMAGE_SIZE_PIXELS
from common.paths import (
    APP_BANNER_IMAGE_PATH,
    APP_ICON_IMAGE_PATH,
    COUNTRY_SHIELD_IMAGE_PATH,
    EMPTY_IMAGE_PATH,
)


def get_image_from_path(image_path: str):
    return ImageTk.PhotoImage(Image.open(image_path))


def get_resized_image(image_path: str):
    image = Image.open(image_path).convert(BASE_IMAGE_MODE)
    base_image = Image.new(
        BASE_IMAGE_MODE,
        (BASE_IMAGE_SIZE_PIXELS, BASE_IMAGE_SIZE_PIXELS),
        BASE_IMAGE_COLOR,  # type: ignore
    )

    image_width, image_height = image.size
    ratio = min(
        BASE_IMAGE_SIZE_PIXELS / image_width,
        BASE_IMAGE_SIZE_PIXELS / image_height,
    )

    new_width = int(image_width * ratio)
    new_height = int(image_height * ratio)
    new_image = image.resize((new_width, new_height))

    x_pos = (BASE_IMAGE_SIZE_PIXELS - new_width) // 2
    y_pos = (BASE_IMAGE_SIZE_PIXELS - new_height) // 2

    base_image.paste(new_image, (x_pos, y_pos), new_image)
    return ImageTk.PhotoImage(base_image)


APP_ICON_IMAGE = get_image_from_path(APP_ICON_IMAGE_PATH)
APP_BANNER_IMAGE = get_image_from_path(APP_BANNER_IMAGE_PATH)
COUNTRY_SHIELD_IMAGE = get_image_from_path(COUNTRY_SHIELD_IMAGE_PATH)
EMPTY_IMAGE = get_resized_image(EMPTY_IMAGE_PATH)

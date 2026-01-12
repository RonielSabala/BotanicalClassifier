from PIL import Image, ImageTk

from common.constants import (
    APP_BANNER_IMAGE_ROUTE,
    APP_ICON_IMAGE_ROUTE,
    COUNTRY_SHIELD_IMAGE_ROUTE,
    EMPTY_IMAGE_ROUTE,
    IMAGE_SIZE,
)


def get_image_from_route(image_route: str):
    return ImageTk.PhotoImage(Image.open(image_route))


def get_resized_image(image_route: str):
    image = Image.open(image_route).convert("RGBA")
    base = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE), (0, 0, 0, 0))  # type: ignore

    original_width, original_height = image.size
    ratio = min(IMAGE_SIZE / original_width, IMAGE_SIZE / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    new_image = image.resize((new_width, new_height))

    x_pos = (IMAGE_SIZE - new_width) // 2
    y_pos = (IMAGE_SIZE - new_height) // 2

    base.paste(new_image, (x_pos, y_pos), new_image)
    return ImageTk.PhotoImage(base)


APP_ICON_IMAGE = get_image_from_route(APP_ICON_IMAGE_ROUTE)
APP_BANNER_IMAGE = get_image_from_route(APP_BANNER_IMAGE_ROUTE)
COUNTRY_SHIELD_IMAGE = get_image_from_route(COUNTRY_SHIELD_IMAGE_ROUTE)
EMPTY_IMAGE = get_resized_image(EMPTY_IMAGE_ROUTE)

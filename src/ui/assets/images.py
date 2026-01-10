from PIL import Image, ImageTk

from common.constants import (
    BANNER_IMG_ROUTE,
    DEFAULT_IMG_SIZE,
    EMPTY_IMG_ROUTE,
    ICON_IMG_ROUTE,
    SHIELD_IMG_ROUTE,
)


def get_image_from_route(image_route: str):
    return ImageTk.PhotoImage(Image.open(image_route))


def get_resized_image(image_route: str):
    image = Image.open(image_route).convert("RGBA")
    base = Image.new("RGBA", (DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE), (0, 0, 0, 0))  # type: ignore

    original_width, original_height = image.size
    ratio = min(DEFAULT_IMG_SIZE / original_width, DEFAULT_IMG_SIZE / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    new_image = image.resize((new_width, new_height))

    x_pos = (DEFAULT_IMG_SIZE - new_width) // 2
    y_pos = (DEFAULT_IMG_SIZE - new_height) // 2

    base.paste(new_image, (x_pos, y_pos), new_image)
    return ImageTk.PhotoImage(base)


# Get images
ICON_IMG = get_image_from_route(ICON_IMG_ROUTE)
EMPTY_IMG = get_resized_image(EMPTY_IMG_ROUTE)
BANNER_IMG = get_image_from_route(BANNER_IMG_ROUTE)
SHIELD_IMG = get_image_from_route(SHIELD_IMG_ROUTE)

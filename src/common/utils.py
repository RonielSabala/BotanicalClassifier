import os
from pathlib import Path
from tkinter import messagebox
from typing import Any

from PIL import Image, ImageTk

from .constants import BASE_IMAGE_COLOR, BASE_IMAGE_MODE, BASE_IMAGE_SIZE_PIXELS


def is_valid_path(path: str | Path) -> bool:
    return os.path.exists(path)


def show_error_messagebox(error_message: str) -> None:
    messagebox.showerror("Error", error_message)


def get_image_from_path(image_path: Path) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(Image.open(image_path))


def get_resized_image(image_path: str | Path) -> ImageTk.PhotoImage:
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


def remove_styles(style: dict[str, Any], to_remove: tuple[str, ...]) -> None:
    for style_to_remove in to_remove:
        try:
            style.pop(style_to_remove)
        except KeyError:
            raise KeyError(f"style ({style}) doesn't has the key '{style_to_remove}'")

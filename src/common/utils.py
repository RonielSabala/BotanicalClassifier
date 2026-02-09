"""
Utility functions used by the GUI.
"""

from collections.abc import Generator, Iterable
from pathlib import Path
from tkinter import messagebox
from typing import Any
from PIL import Image, ImageTk

from .constants import IMAGE_BG_RGBA, IMAGE_MODE, IMAGE_SIZE_PX


def path_exists(path: str | Path) -> bool:
    return Path(path).exists()


def show_error_messagebox(error_message: str) -> None:
    """
    Show an error messagebox.
    """

    messagebox.showerror("Error", error_message)


def load_image_tk(image_path: Path) -> ImageTk.PhotoImage:
    """
    Load an image from `image_path` and return a Tk-compatible
    PhotoImage.
    """

    image = Image.open(image_path).convert(IMAGE_MODE)
    return ImageTk.PhotoImage(image)


def load_resized_image_tk(image_path: str | Path) -> ImageTk.PhotoImage:
    """
    Load an image from `image_path` and resizes it to
    fit inside a square preserving aspect ratio.
    """

    image = Image.open(image_path).convert(IMAGE_MODE)
    base_image = Image.new(
        IMAGE_MODE,
        (IMAGE_SIZE_PX, IMAGE_SIZE_PX),
        IMAGE_BG_RGBA,  # type: ignore
    )

    image_width, image_height = image.size
    ratio = min(IMAGE_SIZE_PX / image_width, IMAGE_SIZE_PX / image_height)

    new_width = int(image_width * ratio)
    new_height = int(image_height * ratio)
    new_image = image.resize((new_width, new_height))

    x_pos = (IMAGE_SIZE_PX - new_width) // 2
    y_pos = (IMAGE_SIZE_PX - new_height) // 2

    base_image.paste(new_image, (x_pos, y_pos), new_image)
    return ImageTk.PhotoImage(base_image)


def remove_keys_from_mapping(
    style: dict[str, Any], to_remove: Iterable[str]
) -> None:
    """
    Remove keys from a mapping in-place.
    """

    for key in to_remove:
        try:
            style.pop(key)
        except KeyError:
            raise KeyError(f"style ({style}) doesn't has the key '{key}'")


def get_subclasses[T](obj: T) -> Generator[T, None, None]:
    """
    Yield all the subclasses of `obj`.
    """

    subclasses = obj.__subclasses__()  # type: ignore
    yield from subclasses
    if not subclasses:
        return

    for subclass in subclasses:
        yield from get_subclasses(subclass)


# Public API
__all__ = (
    "path_exists",
    "show_error_messagebox",
    "load_image_tk",
    "load_resized_image_tk",
    "remove_keys_from_mapping",
    "get_subclasses",
)

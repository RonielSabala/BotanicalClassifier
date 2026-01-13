import os
from tkinter import messagebox
from typing import Generator

from .paths import LOCAL_IMAGES_DIR


def is_valid_path(path: str) -> bool:
    return isinstance(path, str) and os.path.exists(path)


def get_full_image_path(path: str) -> str:
    """
    Devuelve la ruta completa en la carpeta de imágenes.
    """

    return os.path.join(LOCAL_IMAGES_DIR, path)


def get_all_local_images() -> Generator[str, None, None]:
    """
    Devuelve la ruta de todas las imágenes de
    la carpeta imágenes.
    """

    return (get_full_image_path(image) for image in os.listdir(LOCAL_IMAGES_DIR))


def show_error_messagebox(error_message: str) -> None:
    messagebox.showerror("Error", error_message)

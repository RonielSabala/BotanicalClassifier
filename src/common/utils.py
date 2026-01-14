import os
from tkinter import messagebox

from .paths import LOCAL_IMAGES_DIR


def is_valid_path(path: str) -> bool:
    return isinstance(path, str) and os.path.exists(path)


def get_local_image_path(path: str) -> str:
    """
    Devuelve la ruta completa en la carpeta de imágenes.
    """

    return os.path.join(LOCAL_IMAGES_DIR, path)


def show_error_messagebox(error_message: str) -> None:
    messagebox.showerror("Error", error_message)

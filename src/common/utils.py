import os
from typing import Generator

from .constants import LOCAL_STORAGE_IMGS_PATH


def is_valid_path(path: str) -> bool:
    return isinstance(path, str) and os.path.exists(path)


def get_full_image_path(path: str) -> str:
    """
    Devuelve la ruta completa en la carpeta de imágenes.
    """

    return os.path.join(LOCAL_STORAGE_IMGS_PATH, path).replace("\\", "\\\\")


def get_all_images() -> Generator[str, None, None]:
    """
    Devuelve la ruta de todas las imágenes de
    la carpeta imágenes.
    """

    return (get_full_image_path(image) for image in os.listdir(LOCAL_STORAGE_IMGS_PATH))

import os

from .constants import LOCAL_STORAGE_IMGS_ROUTE


def is_valid_route(route: str) -> bool:
    return isinstance(route, str) and os.path.exists(route)


def get_full_image_route(route: str) -> str:
    """
    Devuelve la ruta completa en la carpeta de imágenes.
    """

    return os.path.join(LOCAL_STORAGE_IMGS_ROUTE, route).replace("\\", "\\\\")


def get_all_images():
    """
    Devuelve la ruta de todas las imágenes de
    la carpeta imágenes.
    """

    return (
        get_full_image_route(image) for image in os.listdir(LOCAL_STORAGE_IMGS_ROUTE)
    )

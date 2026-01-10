import os
from tkinter import messagebox

from common.constants import (
    DEFAULT_IMG_SELECT_STR,
    STORAGE_IMGS_ROUTE,
    STORAGE_RECORDS_ROUTE,
)
from common.utils import is_valid_route


def is_valid_field(field: str, name_on_error: str) -> bool:
    """
    Si el campo es válido devuelve True, de otro
    modo False y muestra un error personalizado.
    """

    is_valid = True
    error_msg = f"Ingrese {name_on_error}"
    if not field:
        is_valid = False
        error_msg += "."

    elif len(field) < 5:
        is_valid = False
        error_msg += " con 5 o más caracteres."

    elif len(field) > 50:
        is_valid = False
        error_msg += " de 50 caracteres o menos."

    if not is_valid:
        messagebox.showerror("Error", error_msg)

    return is_valid


def is_valid_name(name: str) -> bool:
    return is_valid_field(name, "un nombre")


def is_valid_last_name(last_name: str) -> bool:
    return is_valid_field(last_name, "un apellido")


def is_valid_location(location: str) -> bool:
    return is_valid_field(location, "una ubicacion")


def is_valid_image_route(image_route: str) -> bool:
    error_msg = ""
    is_valid = True
    if not is_valid_route(image_route):
        is_valid = False
        error_msg = "La ruta de la imagen es invalida."

    elif image_route == DEFAULT_IMG_SELECT_STR:
        is_valid = False
        error_msg = "Ingrese una imagen."

    if not is_valid:
        messagebox.showerror("Error", error_msg)

    return is_valid


def get_images_count() -> int:
    """
    Devuelve el número de archivos de la carpeta imágenes.
    """

    return len(os.listdir(STORAGE_IMGS_ROUTE))


def append_record(record: str) -> None:
    """
    Guarda un registro en el archivo formularios.
    """

    with open(STORAGE_RECORDS_ROUTE, "a") as f:
        f.write(f"{record}\n")

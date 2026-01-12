import os
from tkinter import messagebox

from common.constants import (
    DEFAULT_IMAGE_ENTRY_TEXT,
    IMAGE_PREFIX,
    LOCAL_STORAGE_IMGS_ROUTE,
    LOCAL_STORAGE_RECORDS_ROUTE,
)
from common.utils import is_valid_route

# Entry error messages
ENTER_ENTRY_TEXT = "Ingrese"
ENTER_NAME_TEXT = "un nombre"
ENTER_LAST_NAME_TEXT = "un apellido"
ENTER_LOCATION_TEXT = "una ubicación"
MINIMUM_CHAR_TEXT = "con 5 o más caracteres"
MAXIMUM_CHAR_TEXT = "de 50 caracteres o menos"
DEFAULT_IMAGE_ERROR = "Ingrese una imagen."
INVALID_IMAGE_ROUTE_ERROR = "La ruta de la imagen es invalida."


def show_error(error_message: str) -> None:
    messagebox.showerror("Error", error_message)


def is_valid_entry(entry_name: str, name_on_error: str) -> bool:
    """
    Si el campo es válido devuelve True, de otro
    modo False y muestra un error personalizado.
    """

    is_valid = True
    error_msg = f"{ENTER_ENTRY_TEXT} {name_on_error}"
    if not entry_name:
        is_valid = False

    elif len(entry_name) < 5:
        is_valid = False
        error_msg += " " + MINIMUM_CHAR_TEXT

    elif len(entry_name) > 50:
        is_valid = False
        error_msg += " " + MAXIMUM_CHAR_TEXT

    if not is_valid:
        show_error(error_msg + ".")

    return is_valid


def is_valid_name(name: str) -> bool:
    return is_valid_entry(name, ENTER_NAME_TEXT)


def is_valid_last_name(last_name: str) -> bool:
    return is_valid_entry(last_name, ENTER_LAST_NAME_TEXT)


def is_valid_location(location: str) -> bool:
    return is_valid_entry(location, ENTER_LOCATION_TEXT)


def is_valid_image_route(image_route: str) -> bool:
    error_msg = None
    if image_route == DEFAULT_IMAGE_ENTRY_TEXT:
        error_msg = DEFAULT_IMAGE_ERROR

    elif not is_valid_route(image_route):
        error_msg = INVALID_IMAGE_ROUTE_ERROR

    is_valid = error_msg is None
    if not is_valid:
        show_error(error_msg)

    return is_valid


def get_next_image_filename(img_extension: str) -> str:
    images_count = len(os.listdir(LOCAL_STORAGE_IMGS_ROUTE))
    return f"{IMAGE_PREFIX}_{images_count}.{img_extension}"


def append_record(record: str) -> None:
    """
    Guarda un registro en el archivo formularios.
    """

    with open(LOCAL_STORAGE_RECORDS_ROUTE, "a") as f:
        f.write(f"{record}\n")

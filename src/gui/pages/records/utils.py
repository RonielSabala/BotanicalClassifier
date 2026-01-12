import os
from tkinter import messagebox

from api.predictor import get_flower_prediction
from common.constants import LOCAL_STORAGE_RECORDS_ROUTE
from common.utils import get_all_images

# Error messages
DELETE_IMAGE_ERROR = "Error al eliminar"
RECORD_INDEX_ERROR = "Error al insertar predicción: Número de línea fuera de rango."


def get_records() -> tuple[list, ...]:
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "r") as f:
        return tuple(list(eval(line.strip("\n"))) for line in f.readlines())


def clean_records() -> None:
    """
    Elimina todos los formularios e imágenes.
    """

    # Delete file content
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "w") as f:
        f.write("")

    # Delete record images
    for image in get_all_images():
        try:
            os.unlink(image)
        except Exception as e:
            messagebox.showerror("Error", f"{DELETE_IMAGE_ERROR} {image}: {e}")
            return


def insert_record_prediction(record_index: int) -> None:
    """
    Inserta en el registro de la línea especificada
    la clasificación de la imagen que tiene dicho registro.
    """

    # Get records
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "r") as f:
        records = f.readlines()

    # Validate record index
    if not (0 <= record_index < len(records)):
        messagebox.showerror("Error", RECORD_INDEX_ERROR)
        return

    # - Get prediction:

    record: list[str | list[tuple[str, float]]] = eval(records[record_index])
    flower_image_route = record[-2]
    if not isinstance(flower_image_route, str):
        return

    record[-1] = get_flower_prediction(flower_image_route)

    # Update records
    records[record_index] = f"{record}\n"
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "w") as f:
        f.writelines(records)

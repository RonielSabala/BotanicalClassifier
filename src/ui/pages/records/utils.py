import os

from api.main import get_prediction
from common.constants import LOCAL_STORAGE_RECORDS_ROUTE
from common.utils import get_all_images


def get_records() -> tuple[list, ...]:
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "r") as f:
        return tuple(list(eval(line.strip("\n"))) for line in f.readlines())


def clean_records():
    """
    Elimina todos los formularios e imágenes.
    """

    with open(LOCAL_STORAGE_RECORDS_ROUTE, "w") as f:
        f.write("")

    for image in get_all_images():
        try:
            os.unlink(image)
        except Exception as e:
            print(f"Error al eliminar {image}: {e}")


def insert_classification(line_index: int):
    """
    Inserta en el registro de la línea especificada
    la clasificación de la imagen que tiene dicho registro.
    """

    line_index -= 1
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "r") as f:
        lines = f.readlines()

    if not (0 <= line_index < len(lines)):
        raise ValueError("Error: Número de línea fuera de rango.")

    data = eval(lines[line_index])
    data[-1] = get_prediction(data[-2])
    lines[line_index] = f"{data}\n"

    with open(LOCAL_STORAGE_RECORDS_ROUTE, "w") as f:
        f.writelines(lines)

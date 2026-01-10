from tkinter import messagebox

from common.constants import DEFAULT_IMG
from storage.main import es_ruta


def validar_campo(campo: str, nombre: str) -> bool:
    """
    Si el campo es válido devuelve True, de otro
    modo False y muestra un error personalizado.
    """

    es_valido = True
    mensaje = f"Ingrese {nombre}"

    if not campo:
        es_valido = False
        mensaje += "."

    elif len(campo) < 5:
        es_valido = False
        mensaje += " con 5 o más caracteres."

    elif len(campo) > 50:
        es_valido = False
        mensaje += " de 50 caracteres o menos."

    if not es_valido:
        messagebox.showerror("Error", mensaje)

    return es_valido


def validar_nombre(nombre: str) -> bool:
    return validar_campo(nombre, "un nombre")


def validar_apellido(apellido: str) -> bool:
    return validar_campo(apellido, "un apellido")


def validar_ubicacion(ubicacion: str) -> bool:
    return validar_campo(ubicacion, "una ubicacion")


def validar_imagen(ruta_imagen: str) -> bool:
    es_valida = True
    msg = ""

    if not es_ruta(ruta_imagen):
        es_valida = False
        msg = "La ruta de la imagen es invalida."

    elif ruta_imagen == DEFAULT_IMG:
        es_valida = False
        msg = "Ingrese una imagen."

    if not es_valida:
        messagebox.showerror("Error", msg)

    return es_valida

from PIL import Image, ImageTk

from common.constants import (
    BANNER_IMG_ROUTE,
    DEFAULT_IMG_SIZE,
    EMPTY_IMG_ROUTE,
    ICON_IMG_ROUTE,
    SHIELD_IMG_ROUTE,
)


def obtener_imagen(ruta_imagen: str):
    return ImageTk.PhotoImage(Image.open(ruta_imagen))


def reescalar_imagen(ruta_imagen: str):
    imagen = Image.open(ruta_imagen).convert("RGBA")
    base = Image.new("RGBA", (DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE), (0, 0, 0, 0))  # type: ignore

    ancho_original, alto_original = imagen.size
    ratio = min(DEFAULT_IMG_SIZE / ancho_original, DEFAULT_IMG_SIZE / alto_original)
    nuevo_ancho = int(ancho_original * ratio)
    nuevo_alto = int(alto_original * ratio)

    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))

    pos_x = (DEFAULT_IMG_SIZE - nuevo_ancho) // 2
    pos_y = (DEFAULT_IMG_SIZE - nuevo_alto) // 2

    base.paste(imagen_redimensionada, (pos_x, pos_y), imagen_redimensionada)
    return ImageTk.PhotoImage(base)


# Images
ICON_IMG = obtener_imagen(ICON_IMG_ROUTE)
EMPTY_IMG = reescalar_imagen(EMPTY_IMG_ROUTE)
BANNER_IMG = obtener_imagen(BANNER_IMG_ROUTE)
SHIELD_IMG = obtener_imagen(SHIELD_IMG_ROUTE)

from PIL import Image, ImageTk

from common.constants import (
    IMG_SIZE,
    RUTA_BANNER,
    RUTA_ESCUDO,
    RUTA_ICONO,
    RUTA_VACIO,
)


def obtener_imagen(ruta_imagen: str):
    return ImageTk.PhotoImage(Image.open(ruta_imagen))


def reescalar_imagen(ruta_imagen: str):
    imagen = Image.open(ruta_imagen).convert("RGBA")
    base = Image.new("RGBA", (IMG_SIZE, IMG_SIZE), (0, 0, 0, 0))  # type: ignore

    ancho_original, alto_original = imagen.size
    ratio = min(IMG_SIZE / ancho_original, IMG_SIZE / alto_original)
    nuevo_ancho = int(ancho_original * ratio)
    nuevo_alto = int(alto_original * ratio)

    imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto))

    pos_x = (IMG_SIZE - nuevo_ancho) // 2
    pos_y = (IMG_SIZE - nuevo_alto) // 2

    base.paste(imagen_redimensionada, (pos_x, pos_y), imagen_redimensionada)
    return ImageTk.PhotoImage(base)


# Imágenes
IMG_ICONO = obtener_imagen(RUTA_ICONO)
IMG_ESCUDO = obtener_imagen(RUTA_ESCUDO)
IMG_BANNER = obtener_imagen(RUTA_BANNER)
IMG_VACIO = reescalar_imagen(RUTA_VACIO)

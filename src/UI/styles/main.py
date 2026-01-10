from typing import Any


def actualizar_estilo(
    estilo1: dict[str, Any],
    estilo2: dict[str, Any],
    sobrescribir: bool = False,
) -> dict[str, Any]:
    """
    Actualiza un primer estilo con un segundo estilo.
    """

    estilo1.update(
        {k: v for k, v in estilo2.items() if sobrescribir or k not in estilo1}
    )

    return estilo1


# - Botones:


btn_generico = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white",
    "font": ("Arial", 16, "bold"),
}

btn_primario = {
    "font": ("Arial", 26, "bold"),
    "fg": "black",
    "bg": "goldenrod1",
    "activeforeground": "black",
    "activebackground": "goldenrod3",
}

btn_añadir = {
    "bg": "SpringGreen4",
    "activebackground": "Dark Green",
}

btn_eliminar = {
    "bg": "#b22222",
    "activebackground": "#8b0000",
}

btn_retorno = {
    "text": "↵",
    "font": ("Arial", 25),
    "width": 2,
    "border": 0,
    "relief": "flat",
    "cursor": "hand2",
    "bg": "White",
}

btn_menu = {
    "font": ("Arial", 50),
    "width": 2,
    "border": 0,
    "bg": "White",
    "activebackground": "White",
    "cursor": "hand2",
}


# Agregar el estilo principal a los botones
for btn in (btn_primario, btn_añadir, btn_eliminar):
    actualizar_estilo(btn, btn_generico)


# - Elementos:


# Campo de texto
campo_txt = {
    "width": 22,
    "font": ("Arial", 18),
    "fg": "black",
    "bg": "White",
    "selectforeground": "Black",
    "selectbackground": "GoldenRod1",
}

# Flechas de navegación
flecha_nav = {
    "border": 0,
    "relief": "sunken",
    "fg": "Black",
    "bg": "white",
    "activeforeground": "DodgerBlue4",
    "activebackground": "white",
}


# - Elementos de lista:


list_icono = {
    "font": ("Arial", 32),
    "fg": "DodgerBlue4",
    "bg": "White",
}

list_titulo = {
    "font": ("Arial", 16, "bold"),
    "justify": "left",
    "anchor": "w",
    "padx": 7,
    "pady": 10,
    "bg": "White",
}

list_info = {
    "width": 0,
    "border": 0,
    "font": ("Arial", 12),
    "justify": "left",
    "bg": "White",
}

list_link = {
    "font": ("Arial", 13),
    "width": 0,
    "border": 0,
    "relief": "sunken",
    "cursor": "hand2",
    "fg": "SpringGreen4",
    "activeforeground": "violetred3",
    "activebackground": "White",
    "padx": 0,
    "pady": 0,
    "bg": "White",
}

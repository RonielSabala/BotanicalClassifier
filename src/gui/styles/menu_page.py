from ..tk_enums import MouseType
from .app import page_title

header = {
    "coords": (0.5, 0.01),
    "anchor": "center",
    "font": ("Arial", 9),
}

language = {
    "width": 8,
    "state": "readonly",
    "font": ("Arial", 11),
}

language_label = {
    "anchor": "nw",
    "font": ("Arial", 13),
}

title = {
    **page_title,
    "pady": 10,
}

description = {
    "pady": 25,
    "font": ("Arial", 12),
}

description_separator = {
    "text": "_" * 70,
    "pady": 0,
    "font": ("Arial", 10),
}

question = {
    "pady": 25,
    "font": ("Arial", 15),
}

instructions = {
    "pady": 3,
    "font": ("Arial", 13),
}

_button = {
    "width": 2,
    "border": 0,
    "cursor": MouseType.HAND,
    "font": ("Arial", 50),
}

records_button = {
    **_button,
    "text": "📝",
    "fg": "ivory4",
    "activeforeground": "Gray20",
}

records_button_text = {
    "anchor": "center",
    "font": ("Arial", 14),
}

about_button = {
    **_button,
    "text": "❀",
    "fg": "springGreen4",
    "activeforeground": "violetred4",
}

about_button_text = {
    "anchor": "center",
    "font": ("Arial", 14),
}

exit_button = {
    **_button,
    "width": 3,
    "relief": "sunken",
    "fg": "Red3",
    "font": ("Arial", 18, "underline"),
}

exit_button_text = {
    "text": "⥱",
    "anchor": "center",
    "font": ("Arial", 25),
}

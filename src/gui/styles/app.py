from typing import Any

from ..tk_enums import MouseType

fg_color = "Black"
bg_color = "White"

page_title = {
    "pady": 0,
    "fg": "#091518",
    "font": ("Arial", 35),
}

empty_separator = {
    "text": "",
    "font": ("arial", 0),
}

_generic_button = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": MouseType.CAN_CLICK,
    "font": ("Arial", 16, "bold"),
}

return_button_label: dict[str, Any] = {
    "anchor": "nw",
    "font": ("Arial", 12),
}

return_button = {
    "text": "↵",
    "width": 2,
    "border": 0,
    "anchor": "s",
    "relief": "flat",
    "cursor": MouseType.CAN_CLICK,
    "activebackground": "Gray78",
    "font": ("Arial", 25),
}

primary_button = {
    **_generic_button,
    "bg": "goldenrod1",
    "activebackground": "goldenrod3",
    "font": ("Arial", 26, "bold"),
}

text_entry = {
    "width": 22,
    "selectbackground": "GoldenRod1",
    "font": ("Arial", 18),
}

copyright_text = {
    "coords": (0.5, 0.98),
    "anchor": "center",
    "font": ("Arial", 9),
}

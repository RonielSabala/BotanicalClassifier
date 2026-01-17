from typing import Any

fg_color = "Black"
bg_color = "White"

empty_separator = {
    "text": "",
    "font": ("arial", 0),
}

_generic_button = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": "hand2",
    "font": ("Arial", 16, "bold"),
}

return_button_label: dict[str, Any] = {
    "font": ("Arial", 12),
}

return_button = {
    "text": "↵",
    "width": 2,
    "border": 0,
    "relief": "flat",
    "cursor": "hand2",
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

footer = {
    "coords": (0.5, 0.98),
    "anchor": "center",
    "font": ("Arial", 9),
}

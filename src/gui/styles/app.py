empty_separator = {
    "text": "",
    "fg": "black",
    "font": ("arial", 0),
}

_generic_button = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white",
    "font": ("Arial", 16, "bold"),
}

return_button_label = {
    "fg": "Black",
    "font": ("Arial", 12),
}

return_button = {
    "text": "↵",
    "width": 2,
    "border": 0,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "Black",
    "activebackground": "Gray78",
    "font": ("Arial", 25),
}

primary_button = {
    **_generic_button,
    "fg": "black",
    "bg": "goldenrod1",
    "activeforeground": "black",
    "activebackground": "goldenrod3",
    "font": ("Arial", 26, "bold"),
}

text_entry = {
    "width": 22,
    "fg": "black",
    "selectforeground": "Black",
    "selectbackground": "GoldenRod1",
    "font": ("Arial", 18),
}

footer = {
    "coords": (0.5, 0.98),
    "anchor": "center",
    "fg": "black",
    "font": ("Arial", 9),
}

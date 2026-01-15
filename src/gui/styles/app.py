_generic_button_style = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white",
    "font": ("Arial", 16, "bold"),
}

return_button_label_style = {
    "fg": "Black",
    "font": ("Arial", 12),
}

return_button_style = {
    "text": "↵",
    "width": 2,
    "border": 0,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "Black",
    "activebackground": "Gray78",
    "font": ("Arial", 25),
}

primary_button_style = {
    **_generic_button_style,
    "fg": "black",
    "bg": "goldenrod1",
    "activeforeground": "black",
    "activebackground": "goldenrod3",
    "font": ("Arial", 26, "bold"),
}

entry_text_style = {
    "width": 22,
    "fg": "black",
    "bg": "White",
    "selectforeground": "Black",
    "selectbackground": "GoldenRod1",
    "font": ("Arial", 18),
}

footer_style = {
    "coords": (0.5, 0.98),
    "anchor": "center",
    "fg": "black",
    "font": ("Arial", 9),
}

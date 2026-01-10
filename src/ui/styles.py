# - Buttons:

_btn_generic_style = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white",
    "font": ("Arial", 16, "bold"),
}

btn_primary = {
    "font": ("Arial", 26, "bold"),
    "fg": "black",
    "bg": "goldenrod1",
    "activeforeground": "black",
    "activebackground": "goldenrod3",
}

btn_add = {
    "bg": "SpringGreen4",
    "activebackground": "Dark Green",
}

btn_delete = {
    "bg": "#b22222",
    "activebackground": "#8b0000",
}

btn_return = {
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

# Add generic style to every btn type
for btn_style in (btn_primary, btn_add, btn_delete):
    btn_style.update(
        {k: v for k, v in _btn_generic_style.items() if k not in btn_style}
    )

# - Field elements:

field_text = {
    "width": 22,
    "font": ("Arial", 18),
    "fg": "black",
    "bg": "White",
    "selectforeground": "Black",
    "selectbackground": "GoldenRod1",
}

nav_arrow = {
    "border": 0,
    "relief": "sunken",
    "fg": "Black",
    "bg": "white",
    "activeforeground": "DodgerBlue4",
    "activebackground": "white",
}

# List elements:

list_icon = {
    "font": ("Arial", 32),
    "fg": "DodgerBlue4",
    "bg": "White",
}

list_title = {
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

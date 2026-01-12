# - Buttons:

_button_style = {
    "bd": 0,
    "padx": 5,
    "pady": 2,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "white",
    "activeforeground": "white",
    "font": ("Arial", 16, "bold"),
}

primary_button_style = {
    "font": ("Arial", 26, "bold"),
    "fg": "black",
    "bg": "goldenrod1",
    "activeforeground": "black",
    "activebackground": "goldenrod3",
}

add_button_style = {
    "bg": "SpringGreen4",
    "activebackground": "Dark Green",
}

delete_button_style = {
    "bg": "#b22222",
    "activebackground": "#8b0000",
}

return_button_style = {
    "text": "↵",
    "font": ("Arial", 25),
    "width": 2,
    "border": 0,
    "relief": "flat",
    "cursor": "hand2",
    "bg": "White",
}

menu_button_style = {
    "font": ("Arial", 50),
    "width": 2,
    "border": 0,
    "bg": "White",
    "activebackground": "White",
    "cursor": "hand2",
}

# Add generic style to every button type
for btn_style in (primary_button_style, add_button_style, delete_button_style):
    btn_style.update({k: v for k, v in _button_style.items() if k not in btn_style})

# - Entry elements:

entry_text_style = {
    "width": 22,
    "font": ("Arial", 18),
    "fg": "black",
    "bg": "White",
    "selectforeground": "Black",
    "selectbackground": "GoldenRod1",
}

navigation_arrow_style = {
    "border": 0,
    "relief": "sunken",
    "fg": "Black",
    "bg": "white",
    "activeforeground": "DodgerBlue4",
    "activebackground": "white",
}

# - List elements:

list_emoji_style = {
    "font": ("Arial", 32),
    "fg": "DodgerBlue4",
    "bg": "White",
}

list_title_style = {
    "font": ("Arial", 16, "bold"),
    "justify": "left",
    "anchor": "w",
    "padx": 7,
    "pady": 10,
    "bg": "White",
}

list_info_style = {
    "width": 0,
    "border": 0,
    "font": ("Arial", 12),
    "justify": "left",
    "bg": "White",
}

list_link_style = {
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

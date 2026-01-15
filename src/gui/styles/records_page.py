from .app import _generic_button_style, primary_button_style

add_button_style = {
    **_generic_button_style,
    "bg": "SpringGreen4",
    "activebackground": "Dark Green",
}

delete_button_style = {
    **_generic_button_style,
    "bg": "#b22222",
    "activebackground": "#8b0000",
}

navigation_arrow_style = {
    "border": 0,
    "relief": "sunken",
    "fg": "Black",
    "bg": "white",
    "activeforeground": "DodgerBlue4",
    "activebackground": "white",
    "font": ("Arial", 24),
}

classification_label_style = {
    "text": "N/A",
    "bg": "white",
    "font": ("Arial", 13),
}

classification_button_style = {
    **primary_button_style,
    "fg": "Black",
    "bg": "white",
    "activeforeground": "VioletRed3",
    "activebackground": "white",
    "font": ("Arial", 16, "bold"),
}

column_name_button_style = {
    "border": 0,
    "cursor": "hand2",
    "activeforeground": "Black",
    "activebackground": "DodgerBlue4",
}

search_button_style = {
    "cursor": "hand2",
    "font": ("Arial", 13),
}

page_number_style = {
    "fg": "Black",
    "font": ("Arial", 14),
}

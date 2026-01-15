from .app import _generic_button_style, primary_button_style

default_cell_style = {
    "fg": "Black",
}

column_name_cell_style = {
    "fg": "white",
    "bg": "Dodgerblue4",
}

column_name_button_style = {
    "border": 0,
    "cursor": "hand2",
    "activeforeground": "Black",
    "activebackground": "DodgerBlue4",
}

even_row_cells_style = {
    "fg": "Black",
    "bg": "Gray92",
}

odd_row_cells_style = {
    "fg": "Black",
    "bg": "Gray96",
}

classification_label_style = {
    "text": "N/A",
    "font": ("Arial", 13),
}

classification_button_style = {
    **primary_button_style,
    "fg": "Black",
    "activeforeground": "VioletRed3",
    "font": ("Arial", 16, "bold"),
}

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

search_button_style = {
    "cursor": "hand2",
    "font": ("Arial", 13),
}

navigation_arrow_style = {
    "border": 0,
    "relief": "sunken",
    "fg": "Black",
    "activeforeground": "DodgerBlue4",
    "font": ("Arial", 24),
}

page_number_style = {
    "fg": "Black",
    "font": ("Arial", 14),
}

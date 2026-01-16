from .app import _generic_button_style, primary_button_style

page_title_style = {
    "pady": 0,
    "fg": "#091518",
    "font": ("Arial", 32),
}

default_cell_font = "Segoe UI Emoji", 13
default_cell_style = {
    "fg": "Black",
}

column_name_font = ("Arial", 16, "bold")
column_filter_font = column_name_font + ("underline",)
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
    "font": column_name_font,
}

prediction_cell_style = {
    "fg": "Gray{gray_tone}",
    "bg": "White",
    "font": ("Arial", 10),
}

highest_prediction_cell_style = {
    "fg": "Black",
    "bg": "GoldenRod1",
    "font": ("Arial", 10),
}

tag_column_cell_style = {
    "fg": "White",
    "bg": "Gray15",
    "font": ("Arial", 12, "bold"),
}

probability_column_cell_style = {
    "fg": "GoldenRod1",
    "bg": "Gray15",
    "font": ("Arial", 10, "bold"),
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

from .app import _generic_button, primary_button

title = {
    "pady": 0,
    "fg": "#091518",
    "font": ("Arial", 32),
}

cell_font = "Segoe UI Emoji", 13
cell = {
    "fg": "Black",
}

column_font = ("Arial", 16, "bold")
column_filter_font = column_font + ("underline",)
column_cell = {
    "fg": "white",
    "bg": "Dodgerblue4",
}

column_button = {
    "border": 0,
    "cursor": "hand2",
    "activeforeground": "Black",
    "activebackground": "DodgerBlue4",
}

even_row_cell = {
    "fg": "Black",
    "bg": "Gray92",
}

odd_row_cell = {
    "fg": "Black",
    "bg": "Gray96",
}

classification_label = {
    "text": "N/A",
    "font": ("Arial", 13),
}

classify_button = {
    **primary_button,
    "fg": "Black",
    "activeforeground": "VioletRed3",
    "font": column_font,
}

prediction_cell = {
    "fg": "Gray60",
    "bg": "White",
    "font": ("Arial", 10),
}

top_prediction_cell = {
    "fg": "Black",
    "bg": "GoldenRod1",
    "font": ("Arial", 10),
}

tag_column_cell = {
    "fg": "White",
    "bg": "Gray15",
    "font": ("Arial", 12, "bold"),
}

probability_column_cell = {
    "fg": "GoldenRod1",
    "bg": "Gray15",
    "font": ("Arial", 10, "bold"),
}

add_button = {
    **_generic_button,
    "bg": "SpringGreen4",
    "activebackground": "Dark Green",
}

delete_all_button = {
    **_generic_button,
    "bg": "#b22222",
    "activebackground": "#8b0000",
}

search_button = {
    "cursor": "hand2",
    "font": ("Arial", 13),
}

navigation_arrow = {
    "border": 0,
    "relief": "sunken",
    "fg": "Black",
    "activeforeground": "DodgerBlue4",
    "font": ("Arial", 24),
}

page_indexation = {
    "fg": "Black",
    "font": ("Arial", 14),
}

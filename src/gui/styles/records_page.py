from typing import Any

from common.utils import remove_styles

from .app import _generic_button, primary_button

cell = {}
cell_font = "Segoe UI Emoji", 13

even_row_cell = {
    "bg": "Gray92",
}

odd_row_cell = {
    "bg": "Gray96",
}

first_column_cell_anchor = {
    "padx": 15,
    "anchor": "center",
}

index_column_anchor = {
    "padx": 15,
    "anchor": "e",
}

uploaded_by_column_anchor = {
    "padx": 15,
    "anchor": "w",
}

column_font = "Arial", 16, "bold"
column_filter_font = column_font + ("underline",)
column_cell = {
    "fg": "White",
    "bg": "Dodgerblue4",
}

column_button = {
    "border": 0,
    "cursor": "hand2",
    "activebackground": "DodgerBlue4",
}

classification_label = {
    "text": "N/A",
    "font": ("Arial", 13),
}

classify_button = {
    **primary_button,
    "activeforeground": "VioletRed3",
    "font": column_font,
}
remove_styles(classify_button, ("bg", "activebackground"))

prediction_cell = {
    "fg": "Gray60",
    "font": ("Arial", 10),
}

top_prediction_cell = {
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
    "fg": "White",
    "bg": "SpringGreen4",
    "activeforeground": "White",
    "activebackground": "Dark Green",
}

delete_all_button = {
    **_generic_button,
    "fg": "White",
    "bg": "#b22222",
    "activeforeground": "White",
    "activebackground": "#8b0000",
}

search_button = {
    "cursor": "hand2",
    "bg": "gray90",
    "activebackground": "gray80",
    "font": ("Arial", 13),
}

navigation_arrow = {
    "border": 0,
    "relief": "sunken",
    "activeforeground": "DodgerBlue4",
    "font": ("Arial", 24),
}

page_indexation: dict[str, Any] = {
    "font": ("Arial", 14),
}

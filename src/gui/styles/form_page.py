from .app import text_entry

title = {
    "pady": 15,
    "fg": "#091518",
    "font": ("Arial", 35),
}

name_entry = {
    "pady": 10,
    "fg": "Black",
    "font": ("Arial", 22),
}

select_entry = {
    **text_entry,
    "cursor": "hand2",
    "state": "readonly",
}

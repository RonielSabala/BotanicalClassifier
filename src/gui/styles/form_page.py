from .app import text_entry

title = {
    "pady": 15,
    "fg": "#091518",
    "font": ("Arial", 35),
}

entry_label = {
    "pady": 10,
    "font": ("Arial", 22),
}

image_entry = {
    **text_entry,
    "cursor": "hand2",
    "state": "readonly",
}

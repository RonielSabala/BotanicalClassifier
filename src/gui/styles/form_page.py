from .app import entry_text_style

page_title_style = {
    "pady": 15,
    "fg": "#091518",
    "font": ("Arial", 35),
}

entry_name_style = {
    "pady": 10,
    "fg": "Black",
    "font": ("Arial", 22),
}

select_entry_style = {
    **entry_text_style,
    "cursor": "hand2",
    "state": "readonly",
}

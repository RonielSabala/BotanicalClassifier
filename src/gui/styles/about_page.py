import tkinter as tk

page_title_font = ("Arial", 30)
page_subtitle_font = ("Arial", 15)

emoji_style = {
    "fg": "DodgerBlue4",
    "font": ("Arial", 32),
}

label_style = {
    "padx": 7,
    "pady": 10,
    "anchor": "w",
    "justify": "left",
    "font": ("Arial", 16, "bold"),
}

label_info_style = {
    "width": 0,
    "border": 0,
    "justify": "left",
    "font": ("Arial", 12),
}

link_style = {
    "padx": 0,
    "pady": 0,
    "width": 0,
    "border": 0,
    "relief": "sunken",
    "cursor": "hand2",
    "fg": "SpringGreen4",
    "activeforeground": "violetred3",
    "font": ("Arial", 13),
}

link_separator_style = {
    "fg": "Gray20",
    "font": ("Arial", 16),
}

header_separator_style = {
    "fg": "Gray20",
    "font": ("Arial", 25),
}

about_pages_title_style = {
    "pady": 0,
    "fg": "#091518",
    "font": page_title_font,
}

_scrollable_text_style = {
    "width": 50,
    "height": 12,
    "wrap": tk.WORD,
}

default_scrollable_text_style = {
    **_scrollable_text_style,
    "bg": "Gray95",
    "font": ("Arial", 10),
}

faq_scrollable_text_style = {
    **_scrollable_text_style,
    "relief": "flat",
    "font": ("Arial", 13),
}

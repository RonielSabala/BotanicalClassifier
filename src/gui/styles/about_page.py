import tkinter as tk

from ..tk_enums import MouseType
from .app import page_title

title = {**page_title, "font": ("Arial", 30)}

subtitle_font = ("Arial", 15)

emoji = {"fg": "DodgerBlue4", "font": ("Arial", 32)}

label = {
    "padx": 7,
    "pady": 10,
    "anchor": "w",
    "justify": "left",
    "font": ("Arial", 16, "bold"),
}

label_info = {"width": 0, "border": 0, "justify": "left", "font": ("Arial", 12)}

link = {
    "padx": 0,
    "pady": 0,
    "width": 0,
    "border": 0,
    "relief": "sunken",
    "cursor": MouseType.CAN_CLICK,
    "fg": "SpringGreen4",
    "activeforeground": "violetred3",
    "font": ("Arial", 13),
}

link_separator = {"fg": "Gray20", "font": ("Arial", 16)}

header_separator = {"fg": "Gray20", "font": ("Arial", 25)}

_scrollable_text = {"width": 50, "height": 12, "wrap": tk.WORD}

default_scrollable_text = {**_scrollable_text, "bg": "Gray95", "font": ("Arial", 10)}

faq_scrollable_text = {**_scrollable_text, "relief": "flat", "font": ("Arial", 13)}

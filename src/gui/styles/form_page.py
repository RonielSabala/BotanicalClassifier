from ..tk_enums import CursorType
from .app import page_title, text_entry

title = {**page_title, "pady": 15}

entry_label = {"pady": 10, "font": ("Arial", 22)}

image_entry = {**text_entry, "cursor": CursorType.CAN_CLICK, "state": "readonly"}

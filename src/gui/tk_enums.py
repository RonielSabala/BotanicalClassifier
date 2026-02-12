"""
Simple enums for Tkinter-related constants.
"""

from enum import Enum


class CursorType(str, Enum):
    """
    Common Tkinter mouse cursor types used in the UI.
    """

    DEFAULT = "arrow"
    CAN_CLICK = "hand2"
    CANT_CLICK = "no"
    READ_TEXT = "xterm"


class BindingKey(str, Enum):
    """
    Common Tkinter keyboard events used for widget bindings.
    """

    ARROW_UP = "<Up>"
    ARROW_DOWN = "<Down>"
    ESCAPE = "<Escape>"
    RETURN = "<Return>"
    LEFT_CLICK = "<Button-1>"
    DROP_DOWN_CLICK = "<<ComboboxSelected>>"

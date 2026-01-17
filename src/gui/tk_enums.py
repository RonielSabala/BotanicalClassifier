from enum import Enum


class MouseType(str, Enum):
    DEFAULT = "arrow"
    CAN_CLICK = "hand2"
    CANT_CLICK = "no"
    READ_TEXT = "xterm"


class EventType(str, Enum):
    ARROW_UP = "<Up>"
    ARROW_DOWN = "<Down>"
    ESCAPE = "<Escape>"
    RETURN = "<Return>"
    LEFT_CLICK = "<Button-1>"
    DROP_DOWN_CLICK = "<<ComboboxSelected>>"

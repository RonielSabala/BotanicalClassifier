from enum import Enum


class MouseType(str, Enum):
    HAND = "hand2"


class EventType(str, Enum):
    ARROW_UP = "<Up>"
    ARROW_DOWN = "<Down>"
    ESCAPE = "<Escape>"
    RETURN = "<Return>"
    LEFT_CLICK = "<Button-1>"
    DROP_DOWN_CLICK = "<<ComboboxSelected>>"

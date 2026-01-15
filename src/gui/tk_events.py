from enum import Enum


class EventType(str, Enum):
    ARROW_UP = "<Up>"
    ARROW_DOWN = "<Down>"
    ESCAPE = "<Escape>"
    RETURN = "<Return>"
    LEFT_CLICK = "<Button-1>"

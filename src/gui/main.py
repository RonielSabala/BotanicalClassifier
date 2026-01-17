"""
Main GUI root and shared UI helpers.

This module creates the global Tk root window and a top-level
FRAME used by pages. It also exposes small helpers used by pages.
"""

import tkinter as tk
from datetime import date
from typing import Final

from common.constants import (
    COMPANY_NAME,
    COPYRIGHT_SYMBOL,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from common.paths import APP_ICON_IMAGE_PATH
from services.i18n_service import i18n

# Create root window
ROOT: Final[tk.Tk] = tk.Tk()

# Window centering
_screen_w = ROOT.winfo_screenwidth()
_screen_h = ROOT.winfo_screenheight()
_center_x = int(_screen_w / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
_center_y = int(_screen_h / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT)

# Root properties
_icon_image = tk.PhotoImage(file=APP_ICON_IMAGE_PATH)
ROOT.iconphoto(True, _icon_image)
ROOT.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{_center_x}+{_center_y}")
ROOT.resizable(False, False)

# Root frame used by pages
FRAME: Final[tk.Frame] = tk.Frame(ROOT)
FRAME.pack(fill="both", expand=True)

# Configure FRAME's internal grid so subclasses can use grid inside it
FRAME.grid_rowconfigure(0, weight=1)
FRAME.grid_columnconfigure(0, weight=1)


def set_window_title() -> None:
    """
    Set the main window title for the current language.
    """

    ROOT.title(i18n.get("window.title"))


def _current_year() -> int:
    """
    Return current year at call time.
    """

    return date.today().year


def get_copyright() -> str:
    """
    Build the copyright string.
    """

    year = _current_year()
    rights = i18n.get("app.rights")
    return f"{COMPANY_NAME}\n{COPYRIGHT_SYMBOL}{year} {rights}"


# Public API
__all__ = (
    "ROOT",
    "FRAME",
    "set_window_title",
    "get_copyright",
)

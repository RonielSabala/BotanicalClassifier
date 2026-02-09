"""
Main GUI root and shared UI helpers.
"""

import tkinter as tk
from datetime import date
from typing import Final

from common.constants import (
    COPYRIGHT_SYMBOL,
    ORGANIZATION_NAME,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from common.paths import APP_ICON_IMAGE_PATH
from services.i18n_service import i18n

# Create window root
ROOT: Final[tk.Tk] = tk.Tk()

# Window centering
_screen_w = ROOT.winfo_screenwidth()
_screen_h = ROOT.winfo_screenheight()
_center_x = int(_screen_w / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
_center_y = int(_screen_h / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT)

# Config root properties
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


def get_copyright() -> str:
    """
    Build the copyright string.
    """

    year = date.today().year
    rights = i18n.get("app.rights")
    return f"{ORGANIZATION_NAME}\n{COPYRIGHT_SYMBOL}{year} {rights}"

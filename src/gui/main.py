import tkinter as tk

from common.constants import (
    COMPANY_NAME,
    COPYRIGHT_SYMBOL,
    CURRENT_YEAR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from common.paths import APP_ICON_IMAGE_PATH
from services.i18n_service import i18n

ROOT = tk.Tk()

# Root config
_WINDOW_PADX = int(ROOT.winfo_screenwidth() / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
_WINDOW_PADY = int(ROOT.winfo_screenheight() / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT)
ROOT.iconphoto(True, tk.PhotoImage(file=APP_ICON_IMAGE_PATH))
ROOT.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{_WINDOW_PADX}+{_WINDOW_PADY}")
ROOT.resizable(False, False)

# Root frame
FRAME = tk.Frame(ROOT)
FRAME.pack(fill="both", expand=True)
FRAME.grid_rowconfigure(0, weight=1)
FRAME.grid_columnconfigure(0, weight=1)


def set_window_title() -> None:
    ROOT.title(i18n.get("window.title"))


def get_copyright() -> str:
    rights = i18n.get("app.rights")
    return f"{COMPANY_NAME}\n{COPYRIGHT_SYMBOL}{CURRENT_YEAR} {rights}"

import os
from pathlib import Path
from tkinter import messagebox


def is_valid_path(path: str | Path) -> bool:
    return os.path.exists(path)


def show_error_messagebox(error_message: str) -> None:
    messagebox.showerror("Error", error_message)

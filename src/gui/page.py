import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import scrolledtext, ttk
from typing import Optional

from PIL import ImageTk

from common.constants import (
    COMPANY_NAME,
    COPYRIGHT_SYMBOL,
    CURRENT_YEAR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from common.paths import APP_ICON_IMAGE_PATH
from services.i18n_service import i18n

from .styles import app as app_styles
from .tk_enums import EventType

# App root
APP_ROOT = tk.Tk()

# Root config
_WINDOW_PADX = int(APP_ROOT.winfo_screenwidth() / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
_WINDOW_PADY = int(
    APP_ROOT.winfo_screenheight() / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT
)
APP_ROOT.iconphoto(True, tk.PhotoImage(file=APP_ICON_IMAGE_PATH))
APP_ROOT.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{_WINDOW_PADX}+{_WINDOW_PADY}")
APP_ROOT.resizable(False, False)

# App frame
APP_FRAME = tk.Frame(APP_ROOT)
APP_FRAME.pack(fill="both", expand=True)
APP_FRAME.grid_rowconfigure(0, weight=1)
APP_FRAME.grid_columnconfigure(0, weight=1)


def set_app_title() -> None:
    APP_ROOT.title(i18n.get("window.title"))


def get_app_rights() -> str:
    rights = i18n.get("app.rights")
    return f"{COMPANY_NAME}\n{COPYRIGHT_SYMBOL}{CURRENT_YEAR} {rights}"


class Page(ABC):
    root: tk.Frame
    _is_loaded: bool = False
    main_entry: Optional[tk.Entry] = None
    prev_page: Optional[type["Page"]] = None
    fg_color: str = app_styles.fg_color
    bg_color: str = app_styles.bg_color

    # - Core methods:

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Assign a frame to each subclass
        cls.root = tk.Frame(APP_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    @classmethod
    @abstractmethod
    def load(cls) -> None: ...

    @classmethod
    def close(cls) -> None: ...

    @classmethod
    def destroy(cls) -> None: ...

    @classmethod
    def reset(cls) -> None:
        cls._is_loaded = False
        cls.root.destroy()
        cls.root = tk.Frame(APP_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    @classmethod
    def show(cls) -> None:
        if not cls._is_loaded:
            cls._is_loaded = True
            cls.load()

        cls.root.tkraise()
        cls.root.focus_set()
        cls.root.config(bg=cls.bg_color)

        main_entry = cls.main_entry
        if main_entry is None:
            return

        main_entry.focus_set()
        main_entry.icursor(tk.END)

    # - Utils:

    @classmethod
    def destroy_inner_pages(cls) -> None:
        for page in cls.__subclasses__():
            page.destroy()

    @classmethod
    def get_label(
        cls, root: Optional[tk.Frame] = None, image: Optional[ImageTk.PhotoImage] = None
    ) -> tk.Label:
        if root is None:
            root = cls.root

        if image is None:
            label = tk.Label(root)
        else:
            label = tk.Label(root, image=image)
            label.image = image  # type: ignore

        label.config(fg=cls.fg_color, bg=cls.bg_color)
        return label

    @classmethod
    def get_button(cls, root: Optional[tk.Frame] = None) -> tk.Button:
        if root is None:
            root = cls.root

        return tk.Button(
            root,
            fg=cls.fg_color,
            bg=cls.bg_color,
            activeforeground=cls.fg_color,
            activebackground=cls.bg_color,
        )

    @classmethod
    def get_entry(cls, root: Optional[tk.Frame] = None) -> tk.Entry:
        if root is None:
            root = cls.root

        return tk.Entry(
            root,
            fg=cls.fg_color,
            bg=cls.bg_color,
            selectforeground=cls.fg_color,
        )

    @classmethod
    def get_grid(cls, root: Optional[tk.Frame] = None) -> tk.Frame:
        if root is None:
            root = cls.root

        return tk.Frame(root, bg=cls.bg_color)

    @classmethod
    def get_combobox(cls, *, values: tuple[str, ...]) -> ttk.Combobox:
        return ttk.Combobox(
            cls.root,
            values=values,
            background=cls.bg_color,
            foreground=cls.fg_color,
        )

    @classmethod
    def get_scrollable_text(cls) -> scrolledtext.ScrolledText:
        return scrolledtext.ScrolledText(
            cls.root,
            fg=cls.fg_color,
            bg=cls.bg_color,
        )

    @classmethod
    def set_text(
        cls,
        *,
        text: str,
        pady: int,
        font: tuple[str, int],
        fg: Optional[str] = None,
    ) -> None:
        if fg is None:
            fg = cls.fg_color

        label = cls.get_label()
        label.config(text=text, pady=pady, fg=fg, font=font)
        label.pack()

    @classmethod
    def set_text_at(
        cls,
        *,
        text: str,
        coords: tuple[float, float],
        anchor: str,
        font: tuple[str, int],
        fg: Optional[str] = None,
    ) -> None:
        if fg is None:
            fg = cls.fg_color

        x, y = coords
        label = cls.get_label()
        label.config(text=text, fg=fg, font=font)
        label.place(relx=x, rely=y, anchor=anchor)  # type: ignore

    @classmethod
    def set_app_rights(cls) -> None:
        cls.set_text_at(text=get_app_rights(), **app_styles.footer)

    @classmethod
    def set_return_button(cls) -> None:
        if cls.prev_page is None:
            return

        def _on_escape(event) -> None:
            cls.prev_page.show()  # type: ignore
            cls.close()

        button = cls.get_button()
        button_label = cls.get_label()

        button.config(command=lambda: _on_escape(None), **app_styles.return_button)
        button_label.config(
            text=i18n.get("app.return_button"),
            **app_styles.return_button_label,
        )

        rel_x, rel_y = 0.045, 0.03
        button.place(relx=rel_x, rely=rel_y)
        button_label.place(relx=rel_x, rely=rel_y + 0.07)

        cls.root.bind(EventType.ESCAPE, _on_escape)

    @classmethod
    def set_empty_separator(cls, *, pady: int) -> None:
        label = cls.get_label()
        label.config(pady=pady, **app_styles.empty_separator)
        label.pack()

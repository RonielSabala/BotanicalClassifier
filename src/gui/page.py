from __future__ import annotations

import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import scrolledtext, ttk
from typing import Optional

from PIL import ImageTk

from services.i18n_service import i18n

from .main import FRAME, get_copyright
from .styles import app as app_styles
from .tk_enums import BindingKey


class Page(ABC):
    """
    Abstract base Page class providing common widget factories and
    lifecycle helpers.

    * Class variables:
        - root: The page root. Each subclass will have its own
        frame stored here.

        - _is_loaded: Whether or not the page is already
        loaded.

        - main_entry: Optional main entry widget for focus
        management.

        - prev_page: Optional reference to the previous page
        class.

        - fg_color: Every page widget will have this foreground
        color.

        - bg_color: Every page widget will have this background
        color.
    """

    root: tk.Frame
    _is_loaded: bool = False

    main_entry: Optional[tk.Entry] = None
    prev_page: Optional[type[Page]] = None

    fg_color: str = app_styles.fg_color
    bg_color: str = app_styles.bg_color

    # - Core methods:

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Create a frame attached to the shared FRAME container
        cls.root = tk.Frame(FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    @classmethod
    @abstractmethod
    def load(cls) -> None:
        """
        Load the page.
        """

        ...

    @classmethod
    def close(cls) -> None:
        """
        Optional cleanup when leaving the page.
        """

        ...

    @classmethod
    def reset(cls) -> None:
        """
        Destroy and recreate the page frame so it will be
        rebuilt next time shown.
        """

        cls._is_loaded = False
        cls.root.destroy()
        cls.root = tk.Frame(FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    @classmethod
    def show(cls) -> None:
        """
        Raise the page's frame and set focus on its main entry
        if present.
        """

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

    # - Widget factories:

    @classmethod
    def get_label(
        cls, root: Optional[tk.Frame] = None, image: Optional[ImageTk.PhotoImage] = None
    ) -> tk.Label:
        """
        Return a simple tk.Label widget with `root` as its
        parent and `image` as the widget image. If `root`
        is not provided, uses class' root.
        """

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
        """
        Return a simple tk.Button widget with `root` as its
        parent. If `root` is not provided, uses class' root.
        """

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
        """
        Return a simple tk.Entry widget with `root` as its
        parent. If `root` is not provided, uses class' root.
        """

        if root is None:
            root = cls.root

        return tk.Entry(
            root, fg=cls.fg_color, bg=cls.bg_color, selectforeground=cls.fg_color
        )

    @classmethod
    def get_grid(cls, root: Optional[tk.Frame] = None) -> tk.Frame:
        """
        Return a simple tk.Frame widget with `root` as its
        parent. If `root` is not provided, uses class' root.
        """

        if root is None:
            root = cls.root

        return tk.Frame(root, bg=cls.bg_color)

    @classmethod
    def get_combobox(cls, *, values: tuple[str, ...]) -> ttk.Combobox:
        """
        Return a simple ttk.Combobox widget with the provided
        values.
        """

        return ttk.Combobox(
            cls.root, values=values, background=cls.bg_color, foreground=cls.fg_color
        )

    @classmethod
    def get_scrollable_text(cls) -> scrolledtext.ScrolledText:
        """
        Return a simple scrolledtext.ScrolledText widget.
        """

        return scrolledtext.ScrolledText(cls.root, fg=cls.fg_color, bg=cls.bg_color)

    # - Helpers to place and configure widgets:

    @classmethod
    def set_text(
        cls, *, text: str, pady: int, font: tuple[str, int], fg: Optional[str] = None
    ) -> None:
        """
        Packs a new Label widget in the page.
        """

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
        """
        Places a new Label widget in the page.
        """

        if fg is None:
            fg = cls.fg_color

        x, y = coords
        label = cls.get_label()
        label.config(text=text, fg=fg, font=font)
        label.place(relx=x, rely=y, anchor=anchor)  # type: ignore

    @classmethod
    def set_return_button(cls) -> None:
        """
        Add a small return/back button when `prev_page` is
        provided.
        """

        if cls.prev_page is None:
            return

        def _on_escape(event) -> None:
            """
            Show the previous page and close this page
            """

            cls.prev_page.show()  # type: ignore
            cls.close()

        # Button elements
        button = cls.get_button()
        button_label = cls.get_label()

        # Configuration
        button.config(command=lambda: _on_escape(None), **app_styles.return_button)
        button_label.config(
            text=i18n.get("app.return_button"), **app_styles.return_button_label
        )

        # Bindings
        cls.root.bind(BindingKey.ESCAPE, _on_escape)

        # Layout
        rel_x, rel_y = 0.045, 0.03
        button.place(relx=rel_x, rely=rel_y)
        button_label.place(relx=rel_x, rely=rel_y + 0.07)

    @classmethod
    def set_copyright(cls) -> None:
        """
        Places the copyright text in the page.
        """

        cls.set_text_at(text=get_copyright(), **app_styles.copyright_text)

    @classmethod
    def set_empty_separator(cls, *, pady: int) -> None:
        """
        Packs an empty separator in the page.
        """

        label = cls.get_label()
        label.config(pady=pady, **app_styles.empty_separator)
        label.pack()

import tkinter as tk
from tkinter import Entry, Frame, PhotoImage, ttk
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
APP_ROOT.title(i18n.get("window.title"))
APP_ROOT.iconphoto(True, PhotoImage(file=APP_ICON_IMAGE_PATH))
APP_ROOT.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{_WINDOW_PADX}+{_WINDOW_PADY}")
APP_ROOT.resizable(False, False)

# App frame
APP_FRAME = Frame(APP_ROOT)
APP_FRAME.pack(fill="both", expand=True)
APP_FRAME.grid_rowconfigure(0, weight=1)
APP_FRAME.grid_columnconfigure(0, weight=1)


def get_app_rights() -> str:
    rights = i18n.get("app.rights")
    return f"{COMPANY_NAME}\n{COPYRIGHT_SYMBOL}{CURRENT_YEAR} {rights}"


class Page:
    root: Frame
    prev_page: Optional[type["Page"]] = None
    main_entry: Optional[Entry] = None
    _is_loaded: bool = False
    fg_color: str = app_styles.fg_color
    bg_color: str = app_styles.bg_color

    # - Core methods:

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Assign a frame to each subclass
        cls.root = Frame(APP_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    @classmethod
    def config_pages(cls) -> None:
        """
        Configura las relaciones entre las páginas
        anteriores y posteriores de las páginas
        involucradas en la página actual.
        """
        ...

    @classmethod
    def load(cls) -> None:
        """
        Carga la pagina con todos sus elementos.
        """

        ...

    @classmethod
    def close(cls) -> None:
        """
        Esta función se llama cada vez que se pasa
        de la pagina actual a una pagina anterior.
        """

        ...

    @classmethod
    def destroy(cls) -> None:
        """
        Cuando se va a cerrar la pagina principal
        se llama a esta función para guardar información
        relevante de la pagina en cuestión.
        """

        ...

    @classmethod
    def show(cls) -> None:
        """
        Muestra la pagina.
        """

        if not cls._is_loaded:
            cls.load()
            cls._is_loaded = True

        cls.root.tkraise()
        cls.root.focus_set()
        cls.root.config(bg=cls.bg_color)

        main_entry = cls.main_entry
        if main_entry is None:
            return

        main_entry.focus_set()
        if isinstance(main_entry, Entry):
            main_entry.icursor(tk.END)

    @classmethod
    def reset(cls) -> None:
        """
        Restablece la página dejándola en blanco.
        """

        cls._is_loaded = False
        cls.root.destroy()
        cls.root = Frame(APP_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    # - Utils:

    @classmethod
    def get_label(
        cls, root: Optional[Frame] = None, image: Optional[ImageTk.PhotoImage] = None
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
    def get_button(cls, root: Optional[Frame] = None) -> tk.Button:
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
    def get_entry(cls, root: Optional[Frame] = None) -> Entry:
        if root is None:
            root = cls.root

        return Entry(
            root,
            fg=cls.fg_color,
            bg=cls.bg_color,
            selectforeground=cls.fg_color,
        )

    @classmethod
    def get_grid(cls, root: Optional[Frame] = None) -> Frame:
        if root is None:
            root = cls.root

        return Frame(root, bg=cls.bg_color)

    @classmethod
    def get_combobox(cls, *, values: tuple[str, ...]) -> Entry:
        return ttk.Combobox(
            cls.root,
            values=values,
            background=cls.bg_color,
            foreground=cls.fg_color,
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
        """
        Coloca un texto en la pagina.
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
        Coloca un texto con coordenadas relativas en la pagina.
        """

        if fg is None:
            fg = cls.fg_color

        x, y = coords
        label = cls.get_label()
        label.config(text=text, fg=fg, font=font)
        label.place(relx=x, rely=y, anchor=anchor)  # type: ignore

    @classmethod
    def set_empty_separator(cls, *, pady: int) -> None:
        """
        Coloca un texto en la pagina.
        """

        label = cls.get_label()
        label.config(pady=pady, **app_styles.empty_separator)
        label.pack()

    @classmethod
    def set_footer(cls) -> None:
        cls.set_text_at(text=get_app_rights(), **app_styles.footer)

    @classmethod
    def set_return_btn(cls) -> None:
        """
        Coloca un botón de retorno para ir a la pagina
        anterior. Si se presiona ESC dicho botón es
        activado.
        """

        if cls.prev_page is None:
            return

        def _on_escape(event) -> None:
            if cls.prev_page is not None:
                cls.prev_page.show()

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


def destroy_all_pages():
    """
    Cierra todas las páginas.
    """

    for page in Page.__subclasses__():
        page.destroy()

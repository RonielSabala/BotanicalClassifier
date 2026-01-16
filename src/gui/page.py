import tkinter as tk
from tkinter import Frame, PhotoImage
from typing import Optional

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
from .tk_events import EventType

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
    main_entry: Optional[tk.Entry] = None
    bg_color: str = "White"
    is_loaded: bool = False

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

        if not cls.is_loaded:
            cls.load()
            cls.is_loaded = True

        cls.root.tkraise()
        cls.root.focus_set()
        cls.root.config(bg=cls.bg_color)

        main_entry = cls.main_entry
        if main_entry is None:
            return

        main_entry.focus_set()
        if isinstance(main_entry, tk.Entry):
            main_entry.icursor(tk.END)

    @classmethod
    def reset(cls) -> None:
        """
        Restablece la página dejándola en blanco.
        """

        cls.root.destroy()
        cls.root = Frame(APP_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    # - Utils:

    @classmethod
    def get_grid_from_root(cls) -> Frame:
        return Frame(cls.root, bg=cls.bg_color)

    @classmethod
    def set_text(
        cls,
        *,
        text: str,
        pady: int,
        fg: str,
        font: tuple[str, int],
    ) -> None:
        """
        Coloca un texto en la pagina.
        """

        tk.Label(
            cls.root,
            text=text,
            pady=pady,
            fg=fg,
            bg=cls.bg_color,
            font=font,
        ).pack()

    @classmethod
    def set_text_at(
        cls,
        *,
        text: str,
        coords: tuple[float, float],
        anchor: str,
        fg: str,
        font: tuple[str, int],
    ) -> None:
        """
        Coloca un texto con coordenadas relativas en la pagina.
        """

        label = tk.Label(
            cls.root,
            text=text,
            fg=fg,
            bg=cls.bg_color,
            font=font,
        )

        x, y = coords
        label.place(relx=x, rely=y, anchor=anchor)  # type: ignore

    @classmethod
    def set_empty_separator(cls, *, pady: int) -> None:
        """
        Coloca un texto en la pagina.
        """

        tk.Label(
            cls.root, pady=pady, bg=cls.bg_color, **app_styles.empty_separator
        ).pack()

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

        bg_color = cls.bg_color
        button = tk.Button(
            cls.root,
            command=lambda: _on_escape(None),
            bg=bg_color,
            **app_styles.return_button,
        )

        button_label = tk.Label(
            cls.root,
            text=i18n.get("app.return_button"),
            bg=bg_color,
            **app_styles.return_button_label,
        )

        button.place(relx=0.05, rely=0.05, anchor="nw")
        button_label.place(relx=0.048, rely=0.13, anchor="nw")
        cls.root.bind(EventType.ESCAPE, _on_escape)


def destroy_all_pages():
    """
    Cierra todas las páginas.
    """

    for page in Page.__subclasses__():
        page.destroy()

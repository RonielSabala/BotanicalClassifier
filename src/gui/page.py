import tkinter as tk
from datetime import date
from tkinter import Frame, PhotoImage

from common.constants import APP_ICON_IMAGE_PATH
from services.i18n import i18n

from .styles import return_button_style

# App root
TK_ROOT = tk.Tk()

# Window constants
_WINDOW_WIDTH = 750
_WINDOW_HEIGHT = 900
_MAX_WINDOW_WIDTH = TK_ROOT.winfo_screenwidth()
_MAX_WINDOW_HEIGHT = TK_ROOT.winfo_screenheight()
_WINDOW_PADX = int(_MAX_WINDOW_WIDTH / 2 + _WINDOW_WIDTH / 2 - _WINDOW_WIDTH)
_WINDOW_PADY = int(_MAX_WINDOW_HEIGHT / 2 + _WINDOW_HEIGHT / 2 - _WINDOW_HEIGHT)
TK_ROOT.title(i18n.get("window.title"))
TK_ROOT.iconphoto(False, PhotoImage(file=APP_ICON_IMAGE_PATH))
TK_ROOT.geometry(f"{_WINDOW_WIDTH}x{_WINDOW_HEIGHT}+{_WINDOW_PADX}+{_WINDOW_PADY}")
TK_ROOT.resizable(False, False)

# App frame
TK_FRAME = Frame(TK_ROOT)
TK_FRAME.pack(fill="both", expand=True)
TK_FRAME.grid_rowconfigure(0, weight=1)
TK_FRAME.grid_columnconfigure(0, weight=1)

# Copyright constants
CURRENT_YEAR = date.year
COMPANY_NAME = "Jardín Botánico Nacional"
COPYRIGHT_SYMBOL = "©"


def get_app_rights() -> str:
    rights = i18n.get("app.rights")
    return f"{COMPANY_NAME}\n{COPYRIGHT_SYMBOL}{CURRENT_YEAR} {rights}."


class Page:
    root: Frame
    prev_page: type["Page"] | None = None
    main_entry: None | tk.Entry = None
    bg_color: str = "White"
    is_loaded: bool = False

    # - Core methods:

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Assign a frame to each subclass
        cls.root = Frame(TK_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    @classmethod
    def config_pages(cls):
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
        cls.root = Frame(TK_FRAME)
        cls.root.grid(row=0, column=0, sticky="nsew")

    # - Utils:

    @classmethod
    def get_grid_from_root(cls) -> Frame:
        return Frame(cls.root, bg=cls.bg_color)

    @classmethod
    def set_text(
        cls, text: str, font_size: int, pady: int = 10, fg: str = "cornsilk2"
    ) -> None:
        """
        Coloca un texto en la pagina.
        """

        tk.Label(
            cls.root,
            text=text,
            font=("Arial", font_size),
            bg=cls.bg_color,
            fg=fg,
            pady=pady,
        ).pack()

    @classmethod
    def set_text_at(
        cls,
        text: str,
        font_size: int = 10,
        coordinates: tuple[float, float] = (0.5, 0.5),
        anchor: str = "se",
        fg: str = "white",
    ) -> None:
        """
        Coloca un texto con coordenadas relativas en la pagina.
        """

        text_label = tk.Label(
            cls.root,
            text=text,
            font=("Arial", font_size),
            bg=cls.bg_color,
            fg=fg,
        )

        text_label.place(relx=coordinates[0], rely=coordinates[1], anchor=anchor)  # type: ignore

    @classmethod
    def set_footer(cls):
        cls.set_text_at(get_app_rights(), 9, (0.5, 0.98), anchor="center", fg="black")

    @classmethod
    def set_return_btn(cls, fg: str = "Black") -> None:
        """
        Coloca un botón de retorno para ir a la pagina
        anterior. Si se presiona ESC dicho botón es
        activado.
        """

        if cls.prev_page is None:
            return

        def on_escape(event) -> None:
            cls.prev_page.show()  # type: ignore
            cls.close()

        button = tk.Button(
            cls.root,
            fg=fg,
            command=lambda: on_escape(None),
            activebackground="Gray78",
            **return_button_style,
        )

        button_label = tk.Label(
            cls.root,
            text=i18n.get("app.return_button"),
            font=("Arial", 12),
            fg=fg,
            bg=cls.bg_color,
        )

        button.place(relx=0.05, rely=0.05, anchor="nw")
        button_label.place(relx=0.048, rely=0.13, anchor="nw")
        cls.root.bind("<Escape>", on_escape)


def destroy_all_pages():
    """
    Cierra todas las páginas.
    """

    for page in Page.__subclasses__():
        page.destroy()

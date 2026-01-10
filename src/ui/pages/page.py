import tkinter as tk
from tkinter import PhotoImage
from typing import Type

from common.constants import (
    ICON_IMG_ROUTE,
    WINDOW_FOOTER,
    WINDOW_HEIGHT,
    WINDOW_NAME,
    WINDOW_PADX,
    WINDOW_PADY,
    WINDOW_WIDTH,
)

from ..styles import btn_retorno

TK_ROOT = tk.Tk()
TK_ROOT.title(WINDOW_NAME)
TK_ROOT.iconphoto(True, PhotoImage(file=ICON_IMG_ROUTE))
TK_ROOT.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_PADX}+{WINDOW_PADY}")
TK_ROOT.resizable(False, False)

# Page frame
TK_FRAME = tk.Frame(TK_ROOT)
TK_FRAME.pack(fill="both", expand=True)
TK_FRAME.grid_rowconfigure(0, weight=1)
TK_FRAME.grid_columnconfigure(0, weight=1)


class Page:
    raiz: tk.Frame
    fue_cargada: bool = False
    pagina_anterior: Type["Page"] | None = None
    pagina_posterior: Type["Page"] | None = None
    color_fondo: str = "White"
    color_fondo_opaco: str = "Gray78"
    main_element: None | tk.Entry = None

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Asignar un Frame del contenedor a cada subclase
        cls.raiz = tk.Frame(TK_FRAME)
        cls.raiz.grid(row=0, column=0, sticky="nsew")

    @classmethod
    def load(cls) -> None:
        """
        Carga la pagina con todos sus elementos.
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
    def close(cls) -> None:
        """
        Esta función se llama cada vez que se pasa
        de la pagina actual a una pagina anterior.
        """

        ...

    @classmethod
    def show(cls) -> None:
        """
        Muestra la pagina.
        """

        if cls.fue_cargada is False:
            cls.load()
            cls.fue_cargada = True

        cls.raiz.tkraise()
        cls.raiz.focus_set()
        cls.raiz.config(bg=cls.color_fondo)
        item = cls.main_element
        if item is not None:
            item.focus_set()

            if isinstance(item, tk.Entry):
                item.icursor(tk.END)

    @classmethod
    def reset(cls) -> None:
        """
        Restablece la página dejándola en blanco.
        """

        cls.raiz.destroy()
        cls.raiz = tk.Frame(TK_FRAME)
        cls.raiz.grid(row=0, column=0, sticky="nsew")

    @classmethod
    def config_pages(cls):
        """
        Configura las relaciones entre las páginas
        anteriores y posteriores de las páginas
        involucradas en la página actual.
        """
        ...

    @classmethod
    def set_text(
        cls, text: str, size: int, pady: int = 10, fg: str = "cornsilk2"
    ) -> None:
        """
        Coloca un texto en la pagina.
        """

        tk.Label(
            cls.raiz,
            text=text,
            font=("Arial", size),
            bg=cls.color_fondo,
            fg=fg,
            pady=pady,
        ).pack()

    @classmethod
    def set_text_at(
        cls,
        text: str,
        size: int = 10,
        coordinates: tuple[float, float] = (0.5, 0.5),
        anchor: str = "se",
        fg: str = "white",
    ) -> None:
        """
        Coloca un texto con coordenadas relativas en la pagina.
        """

        label = tk.Label(
            cls.raiz,
            text=text,
            font=("Arial", size),
            bg=cls.color_fondo,
            fg=fg,
        )

        label.place(relx=coordinates[0], rely=coordinates[1], anchor=anchor)  # type: ignore

    @classmethod
    def set_return_btn(cls, fg: str = "Black") -> None:
        """
        Coloca un botón de retorno para ir a la pagina
        anterior. Si se presiona ESC dicho botón es
        activado.
        """

        if cls.pagina_anterior is None:
            return

        def escape_event(event) -> None:
            cls.pagina_anterior.show()  # type: ignore
            cls.close()

        text = tk.Label(
            cls.raiz, text="Volver", font=("Arial", 12), fg=fg, bg=cls.color_fondo
        )

        btn = tk.Button(
            cls.raiz,
            fg=fg,
            command=lambda: escape_event(None),
            activebackground=cls.color_fondo_opaco,
            **btn_retorno,
        )

        cls.raiz.bind("<Escape>", escape_event)
        text.place(relx=0.048, rely=0.13, anchor="nw")
        btn.place(relx=0.05, rely=0.05, anchor="nw")

    @classmethod
    def set_footer(cls):
        cls.set_text_at(WINDOW_FOOTER, 9, (0.5, 0.98), anchor="center", fg="black")

    @classmethod
    def get_grid(cls):
        return tk.Frame(cls.raiz, bg=cls.color_fondo)


def destroy_all_pages():
    """
    Cierra todas las páginas.
    """

    for page in Page.__subclasses__():
        page.destroy()

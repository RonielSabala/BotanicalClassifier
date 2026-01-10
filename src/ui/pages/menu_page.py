import tkinter as tk
from tkinter import font

from ..assets.main import BANNER_IMG
from ..styles import btn_menu, btn_primario
from .page import TK_ROOT, Page, destroy_all_pages


class Menu(Page):
    @classmethod
    def show(cls) -> None:
        cls.config_pages()
        super().show()

    @classmethod
    def destroy(cls) -> None:
        TK_ROOT.destroy()

    @classmethod
    def config_pages(cls):
        from .form.form_page import Form

        Form.pagina_anterior = cls

    @classmethod
    def load(cls) -> None:
        from .contact.contact_page import Contact
        from .form.form_page import Form
        from .table_page import Table

        # - Header:

        tk.Label(cls.raiz, image=BANNER_IMG, bg=cls.color_fondo).pack(padx=10, pady=5)
        cls.set_text_at(
            "Presidencia de la República: www.presidencia.gob.do",
            9,
            (0.5, 0.01),
            anchor="center",
            fg="black",
        )

        cls.set_text("Flor survey", 35, pady=10, fg="#091518")
        cls.set_text(
            "Estamos realizando una investigación a nivel nacional para calcular\n"
            + "la cantidad de flores de cada tipo que tienen las personas en sus\n"
            + "hogares.",
            12,
            pady=25,
            fg="#091518",
        )

        cls.set_text("_" * 70, 10, pady=0, fg="#091518")
        cls.set_text(
            "¿Te gustaría participar?",
            15,
            pady=25,
            fg="#091518",
        )

        cls.set_text(
            "Solo tienes que completar la siguiente encuesta:",
            13,
            pady=3,
            fg="#091518",
        )

        cls.set_text("", 13, pady=15, fg="#091518")

        # - Creación de los botones:

        btn_formulario = tk.Button(
            cls.raiz,
            text="Llenar encuesta",
            command=Form.show,
            **btn_primario,
        )

        btn_registros = tk.Button(
            cls.raiz,
            text="📝",
            command=Table.show,
            fg="ivory4",
            activeforeground="Gray20",
            **btn_menu,
        )

        btn_sobre_nosotros = tk.Button(
            cls.raiz,
            text="❀",
            command=Contact.show,
            fg="springGreen4",
            activeforeground="violetred4",
            **btn_menu,
        )

        btn_salir = tk.Button(
            cls.raiz,
            text="Salir",
            command=destroy_all_pages,
            fg="Red3",
            activeforeground="black",
            relief="sunken",
            **btn_menu,
        )

        # - Configuración:

        btn_formulario.pack(pady=0)

        # Botón de registros
        x, y = 0.5, 0.73
        btn_registros.place(relx=x, rely=y, anchor="center")
        cls.set_text_at(
            "Registros", 14, (x - 0.01, y + 0.06), anchor="center", fg="black"
        )

        # Botón sobre nosotros
        x, y = 0.1, 0.9
        btn_sobre_nosotros.place(relx=x, rely=y, anchor="center")
        cls.set_text_at(
            "Sobre\nnosotros", 14, (x, y + 0.06), anchor="center", fg="black"
        )

        # Botón de salir
        x, y = 0.92, 0.94
        btn_salir.config(
            font=font.Font(family="Arial", size=18, underline=True), width=3
        )
        btn_salir.place(relx=x, rely=y, anchor="center")
        cls.set_text_at(
            "⥱", 25, (x, y + 0.04), anchor="center", fg=btn_salir.cget("fg")
        )

        # - Footer:

        cls.set_footer()

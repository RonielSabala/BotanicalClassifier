import tkinter as tk
from tkinter import font

from ..assets.images import BANNER_IMG
from ..styles import btn_menu, btn_primary
from .page import TK_ROOT, Page, destroy_all_pages

# Page content
COUNTRY_URL = "Presidencia de la República: www.presidencia.gob.do"
PAGE_TITLE = "Flor survey"
PAGE_DESCRIPTION = """Estamos realizando una investigación a nivel nacional para calcular
la cantidad de flores de cada tipo que tienen las personas en sus
hogares."""

DESCRIPTION_SEPARATION = "_" * 70
PAGE_HOOK = "¿Te gustaría participar?"
PAGE_INSTRUCTIONS = "Solo tienes que completar la siguiente encuesta:"


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

        Form.prev_page = cls

    @classmethod
    def load(cls) -> None:
        from .contact.contact_page import Contact
        from .form.form_page import Form
        from .table.table_page import Table

        # Header
        tk.Label(cls.root, image=BANNER_IMG, bg=cls.bg_color).pack(padx=10, pady=5)
        cls.set_text_at(COUNTRY_URL, 9, (0.5, 0.01), anchor="center", fg="black")
        cls.set_text(PAGE_TITLE, 35, pady=10, fg="#091518")
        cls.set_text(PAGE_DESCRIPTION, 12, pady=25, fg="#091518")
        cls.set_text(DESCRIPTION_SEPARATION, 10, pady=0, fg="#091518")
        cls.set_text(PAGE_HOOK, 15, pady=25, fg="#091518")
        cls.set_text(PAGE_INSTRUCTIONS, 13, pady=3, fg="#091518")
        cls.set_text("", 13, pady=15, fg="#091518")

        # - Create buttons:

        btn_form = tk.Button(
            cls.root, text="Llenar encuesta", command=Form.show, **btn_primary
        )

        btn_records = tk.Button(
            cls.root,
            text="📝",
            command=Table.show,
            fg="ivory4",
            activeforeground="Gray20",
            **btn_menu,
        )

        btn_about = tk.Button(
            cls.root,
            text="❀",
            command=Contact.show,
            fg="springGreen4",
            activeforeground="violetred4",
            **btn_menu,
        )

        btn_exit = tk.Button(
            cls.root,
            text="Salir",
            command=destroy_all_pages,
            fg="Red3",
            activeforeground="black",
            relief="sunken",
            **btn_menu,
        )

        # - Configure elements:

        btn_form.pack(pady=0)

        # Records btn
        x, y = 0.5, 0.73
        btn_records.place(relx=x, rely=y, anchor="center")
        cls.set_text_at(
            "Registros", 14, (x - 0.01, y + 0.06), anchor="center", fg="black"
        )

        # About btn
        x, y = 0.1, 0.9
        btn_about.place(relx=x, rely=y, anchor="center")
        cls.set_text_at(
            "Sobre\nnosotros", 14, (x, y + 0.06), anchor="center", fg="black"
        )

        # Exit btn
        x, y = 0.92, 0.94
        btn_exit.config(
            font=font.Font(family="Arial", size=18, underline=True), width=3
        )
        btn_exit.place(relx=x, rely=y, anchor="center")
        cls.set_text_at("⥱", 25, (x, y + 0.04), anchor="center", fg=btn_exit.cget("fg"))

        cls.set_footer()

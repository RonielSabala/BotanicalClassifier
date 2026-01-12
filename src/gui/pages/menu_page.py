import tkinter as tk
from tkinter import font

from ..assets.loaded_images import APP_BANNER_IMAGE
from ..styles import menu_button_style, primary_button_style
from .page import TK_ROOT, Page, destroy_all_pages

# - Page info:

COUNTRY_URL_PAGE = "Presidencia de la República: www.presidencia.gob.do"
PAGE_TITLE = "Flor survey"
PAGE_DESCRIPTION = """Estamos realizando una investigación a nivel nacional para calcular\nla cantidad de flores de cada tipo que\ntienen las personas en sus\nhogares."""

PAGE_QUESTION = "¿Te gustaría participar?"
PAGE_INSTRUCTIONS = "Solo tienes que completar la siguiente encuesta:"

# - Page elements:

FORM_BUTTON_TEXT = "Llenar encuesta"

RECORDS_LABEL = "Registros"
RECORDS_BUTTON_TEXT = "📝"

ABOUT_LABEL = "Sobre\nnosotros"
ABOUT_BUTTON_TEXT = "❀"

EXIT_LABEL = "⥱"
EXIT_BUTTON_TEXT = "Salir"


class MenuPage(Page):
    fg_text_color = "#091518"

    @classmethod
    def show(cls) -> None:
        cls.config_pages()
        super().show()

    @classmethod
    def destroy(cls) -> None:
        TK_ROOT.destroy()

    @classmethod
    def config_pages(cls):
        from .form.form_page import FormPage

        FormPage.prev_page = cls

    @classmethod
    def load(cls) -> None:
        from .about.about_page import AboutPage
        from .form.form_page import FormPage
        from .records.records_page import Records

        # - Header elements:

        tk.Label(cls.root, image=APP_BANNER_IMAGE, bg=cls.bg_color).pack(
            padx=10, pady=5
        )
        cls.set_text_at(
            COUNTRY_URL_PAGE, 9, (0.5, 0.01), anchor="center", fg=cls.fg_text_color
        )

        cls.set_text(PAGE_TITLE, 35, pady=10, fg=cls.fg_text_color)
        cls.set_text(PAGE_DESCRIPTION, 12, pady=25, fg=cls.fg_text_color)
        cls.set_text("_" * 70, 10, pady=0, fg=cls.fg_text_color)

        cls.set_text(PAGE_QUESTION, 15, pady=25, fg=cls.fg_text_color)
        cls.set_text(PAGE_INSTRUCTIONS, 13, pady=3, fg=cls.fg_text_color)
        cls.set_text("", 13, pady=15)

        # - Page elements:

        form_button = tk.Button(
            cls.root,
            text=FORM_BUTTON_TEXT,
            command=FormPage.show,
            **primary_button_style,
        )

        records_button = tk.Button(
            cls.root,
            text=RECORDS_BUTTON_TEXT,
            command=Records.show,
            fg="ivory4",
            activeforeground="Gray20",
            **menu_button_style,
        )

        about_button = tk.Button(
            cls.root,
            text=ABOUT_BUTTON_TEXT,
            command=AboutPage.show,
            fg="springGreen4",
            activeforeground="violetred4",
            **menu_button_style,
        )

        exit_button = tk.Button(
            cls.root,
            text=EXIT_BUTTON_TEXT,
            command=destroy_all_pages,
            fg="Red3",
            activeforeground="black",
            relief="sunken",
            **menu_button_style,
        )

        # - Elements configuration:

        # Form button
        form_button.pack(pady=0)

        # Records button
        rel_x, rel_y = 0.5, 0.74
        records_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            RECORDS_LABEL, 14, (rel_x - 0.01, rel_y + 0.06), anchor="center", fg="black"
        )

        # About button
        rel_x, rel_y = 0.1, 0.9
        about_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            ABOUT_LABEL, 14, (rel_x, rel_y + 0.06), anchor="center", fg="black"
        )

        # Exit button
        rel_x, rel_y = 0.92, 0.94
        exit_button.config(
            font=font.Font(family="Arial", size=18, underline=True), width=3
        )

        exit_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            EXIT_LABEL,
            25,
            (rel_x, rel_y + 0.04),
            anchor="center",
            fg=exit_button.cget("fg"),
        )

        cls.set_footer()

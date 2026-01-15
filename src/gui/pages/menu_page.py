import tkinter as tk

from services.i18n_service import i18n

from ..assets.images import APP_BANNER_IMAGE
from ..page import APP_ROOT, Page, destroy_all_pages
from ..styles.app import primary_button_style
from ..styles.menu_page import (
    about_button_style,
    about_button_text_style,
    exit_button_style,
    exit_button_text_style,
    header_text_style,
    records_button_style,
    records_button_text_style,
)


class MenuPage(Page):
    @classmethod
    def show(cls) -> None:
        cls.config_pages()
        super().show()

    @classmethod
    def destroy(cls) -> None:
        APP_ROOT.destroy()

    @classmethod
    def config_pages(cls) -> None:
        from .form_page import FormPage

        FormPage.prev_page = cls

    @classmethod
    def load(cls) -> None:
        from .about_page import AboutPage
        from .form_page import FormPage
        from .records_page import RecordsPage

        bg_color = cls.bg_color
        fg_color = "#091518"

        # - Header elements:

        tk.Label(cls.root, image=APP_BANNER_IMAGE, bg=bg_color).pack(padx=10, pady=5)
        page_header = i18n.get("menu.header")
        cls.set_text_at(text=page_header, fg=fg_color, **header_text_style)

        page_title = i18n.get("menu.title")
        page_description = i18n.get("menu_description")
        cls.set_text(text=page_title, pady=10, fg=fg_color, font=("Arial", 35))
        cls.set_text(text=page_description, pady=25, fg=fg_color, font=("Arial", 12))
        cls.set_text(text="_" * 70, pady=0, fg=fg_color, font=("Arial", 10))

        page_question = i18n.get("menu.survey_question")
        page_instructions = i18n.get("menu.survey_instructions")
        cls.set_text(text=page_question, pady=25, fg=fg_color, font=("Arial", 15))
        cls.set_text(text=page_instructions, pady=3, fg=fg_color, font=("Arial", 13))
        cls.set_empty_separator(pady=20)

        # - Page elements:

        form_button = tk.Button(
            cls.root,
            text=i18n.get("menu.form_button"),
            command=FormPage.show,
            **primary_button_style,
        )

        records_button = tk.Button(
            cls.root,
            command=RecordsPage.show,
            bg=bg_color,
            activebackground=bg_color,
            **records_button_style,
        )

        about_button = tk.Button(
            cls.root,
            command=AboutPage.show,
            bg=bg_color,
            activebackground=bg_color,
            **about_button_style,
        )

        exit_button = tk.Button(
            cls.root,
            text=i18n.get("menu.exit_button"),
            command=destroy_all_pages,
            bg=bg_color,
            activebackground=bg_color,
            **exit_button_style,
        )

        # - Elements configuration:

        form_button.pack(pady=0)

        # Records button
        rel_x, rel_y = 0.5, 0.74
        records_button_label = i18n.get("menu.records_button")
        records_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            text=records_button_label,
            coords=(rel_x - 0.01, rel_y + 0.06),
            **records_button_text_style,
        )

        # About button
        rel_x, rel_y = 0.1, 0.9
        about_button_label = i18n.get("menu.about_button")
        about_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            text=about_button_label,
            coords=(rel_x, rel_y + 0.06),
            **about_button_text_style,
        )

        # Exit button
        rel_x, rel_y = 0.92, 0.94
        exit_button.config(font=("Arial", 18, "underline"), width=3)
        exit_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            coords=(rel_x, rel_y + 0.04),
            fg=exit_button.cget("fg"),
            **exit_button_text_style,
        )

        cls.set_footer()

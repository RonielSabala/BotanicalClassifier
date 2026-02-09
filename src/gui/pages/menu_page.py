"""
Main menu page of the application.
"""

import tkinter as tk

from common.utils import get_subclasses
from services import Language, i18n

from ..assets import APP_BANNER_IMAGE
from ..main import ROOT, set_window_title
from ..page import Page
from ..styles import app as app_styles, menu_page as page_styles
from ..tk_enums import EventType


class MenuPage(Page):
    _language_var = tk.StringVar(value=i18n.default)

    # - Event handlers:

    @classmethod
    def _on_language_select(cls) -> None:
        """
        Handle language selection changes. Resets all pages
        so they reload their UI with the new language.
        """

        lang = cls._language_var.get()
        if lang == i18n.current_language:
            return

        i18n.set_language(lang)

        # Reset all pages
        for page in get_subclasses(Page):
            page.reset()

        set_window_title()
        super().show()

    # - Overridden methods:

    @classmethod
    def show(cls) -> None:
        from .form_page import FormPage

        # Configure back-navigation for the form page
        FormPage.prev_page = cls

        super().show()

    @classmethod
    def load(cls) -> None:
        from .about_page import AboutPage
        from .form_page import FormPage
        from .records_page import RecordsPage

        # - Widgets:

        page_banner = cls.get_label(image=APP_BANNER_IMAGE)

        lang_combobox = cls.get_combobox(values=Language.all_languages())
        form_button = cls.get_button()
        records_button = cls.get_button()
        about_button = cls.get_button()
        exit_button = cls.get_button()

        # - Configuration:

        lang_combobox.config(textvariable=cls._language_var, **page_styles.language)
        form_button.config(
            text=i18n.get("menu.form_button"),
            command=FormPage.show,
            **app_styles.primary_button,
        )

        records_button.config(command=RecordsPage.show, **page_styles.records_button)

        about_button.config(command=AboutPage.show, **page_styles.about_button)

        exit_button.config(
            text=i18n.get("menu.exit_button"),
            command=ROOT.destroy,
            **page_styles.exit_button,
        )

        # Bindings
        lang_combobox.bind(
            EventType.DROP_DOWN_CLICK, lambda _: cls._on_language_select()
        )

        # - Layout:

        # Header
        page_banner.pack(padx=10, pady=5)
        cls.set_text_at(text=i18n.get("menu.header"), **page_styles.header)
        cls.set_text(text=i18n.get("menu.title"), **page_styles.title)
        cls.set_text(text=i18n.get("menu.description"), **page_styles.description)
        cls.set_text(**page_styles.description_separator)
        cls.set_text(text=i18n.get("menu.question"), **page_styles.question)
        cls.set_text(text=i18n.get("menu.instructions"), **page_styles.instructions)
        cls.set_empty_separator(pady=20)

        # Language selector
        cls.set_text_at(
            text=i18n.get("app.language"), coords=(0, 0), **page_styles.language_label
        )
        lang_combobox.place(relx=0.005, rely=0.03)

        # Form button
        form_button.pack(pady=0)

        # Records button
        records_x, records_y = 0.5, 0.74
        records_button.place(relx=records_x, rely=records_y, anchor="center")
        cls.set_text_at(
            text=i18n.get("menu.records_button"),
            coords=(records_x - 0.01, records_y + 0.06),
            **page_styles.records_button_text,
        )

        # About button
        about_x, about_y = 0.1, 0.9
        about_button.place(relx=about_x, rely=about_y, anchor="center")
        cls.set_text_at(
            text=i18n.get("menu.about_button"),
            coords=(about_x, about_y + 0.06),
            **page_styles.about_button_text,
        )

        # Exit button
        exit_x, exit_y = 0.92, 0.94
        exit_button.place(relx=exit_x, rely=exit_y, anchor="center")
        cls.set_text_at(
            coords=(exit_x, exit_y + 0.04),
            fg=exit_button.cget("fg"),
            **page_styles.exit_button_text,
        )

        cls.set_copyright()

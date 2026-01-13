import tkinter as tk
from tkinter import font

from services.i18n import i18n

from ..assets.images import APP_BANNER_IMAGE
from ..page import APP_ROOT, Page, destroy_all_pages
from ..styles import menu_button_style, primary_button_style

# GUI defaults
RECORDS_BUTTON_TEXT = "📝"
ABOUT_BUTTON_TEXT = "❀"
EXIT_BUTTON_LABEL = "⥱"
FG_COLOR = "#091518"


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
        from .form.form_page import FormPage

        FormPage.prev_page = cls

    @classmethod
    def load(cls) -> None:
        from .about_page import AboutPage
        from .form.form_page import FormPage
        from .records.records_page import RecordsPage

        # - Header elements:

        tk.Label(cls.root, image=APP_BANNER_IMAGE, bg=cls.bg_color).pack(
            padx=10, pady=5
        )

        page_header = i18n.get("menu.header")
        cls.set_text_at(page_header, 9, (0.5, 0.01), anchor="center", fg=FG_COLOR)

        page_title = i18n.get("menu.title")
        page_description = i18n.get("menu_description")
        cls.set_text(page_title, 35, pady=10, fg=FG_COLOR)
        cls.set_text(page_description, 12, pady=25, fg=FG_COLOR)
        cls.set_text("_" * 70, 10, pady=0, fg=FG_COLOR)

        page_question = i18n.get("menu.survey_question")
        page_instructions = i18n.get("menu.survey_instructions")
        cls.set_text(page_question, 15, pady=25, fg=FG_COLOR)
        cls.set_text(page_instructions, 13, pady=3, fg=FG_COLOR)
        cls.set_text("", 13, pady=15)

        # - Page elements:

        form_button_text = i18n.get("menu.form_button")
        form_button = tk.Button(
            cls.root,
            text=form_button_text,
            command=FormPage.show,
            **primary_button_style,
        )

        records_button = tk.Button(
            cls.root,
            text=RECORDS_BUTTON_TEXT,
            command=RecordsPage.show,
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

        exit_button_text = i18n.get("menu.exit_button")
        exit_button = tk.Button(
            cls.root,
            text=exit_button_text,
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
        records_button_label = i18n.get("menu.records_button")
        records_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            records_button_label,
            14,
            (rel_x - 0.01, rel_y + 0.06),
            anchor="center",
            fg="black",
        )

        # About button
        rel_x, rel_y = 0.1, 0.9
        about_button_label = i18n.get("menu.about_button")
        about_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            about_button_label,
            14,
            (rel_x, rel_y + 0.06),
            anchor="center",
            fg="black",
        )

        # Exit button
        rel_x, rel_y = 0.92, 0.94
        exit_button.config(
            font=font.Font(family="Arial", size=18, underline=True), width=3
        )

        exit_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            EXIT_BUTTON_LABEL,
            25,
            (rel_x, rel_y + 0.04),
            anchor="center",
            fg=exit_button.cget("fg"),
        )

        cls.set_footer()

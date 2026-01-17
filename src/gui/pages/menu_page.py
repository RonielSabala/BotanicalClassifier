from services.i18n_service import i18n

from ..assets.images import APP_BANNER_IMAGE
from ..page import APP_ROOT, Page, destroy_all_pages
from ..styles import app as app_styles
from ..styles import menu_page as page_styles


class MenuPage(Page):
    fg_color = page_styles.fg_color

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

        # - Header elements:

        cls.get_label(image=APP_BANNER_IMAGE).pack(padx=10, pady=5)
        cls.set_text_at(text=i18n.get("menu.header"), **page_styles.header)

        page_title = i18n.get("menu.title")
        page_description = i18n.get("menu_description")
        cls.set_text(text=page_title, **page_styles.title)
        cls.set_text(text=page_description, **page_styles.description)
        cls.set_text(**page_styles.description_separator)

        page_question = i18n.get("menu.survey_question")
        page_instructions = i18n.get("menu.survey_instructions")
        cls.set_text(text=page_question, **page_styles.question)
        cls.set_text(text=page_instructions, **page_styles.instructions)
        cls.set_empty_separator(pady=20)

        # Page buttons
        form_button = cls.get_button()
        records_button = cls.get_button()
        about_button = cls.get_button()
        exit_button = cls.get_button()

        # - Elements configuration:

        # Form button
        form_button.config(
            text=i18n.get("menu.form_button"),
            command=FormPage.show,
            **app_styles.primary_button,
        )
        form_button.pack(pady=0)

        # Records button
        rel_x, rel_y = 0.5, 0.74
        records_button.config(
            command=RecordsPage.show,
            **page_styles.records_button,
        )
        records_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            text=i18n.get("menu.records_button"),
            coords=(rel_x - 0.01, rel_y + 0.06),
            **page_styles.records_button_text,
        )

        # About button
        rel_x, rel_y = 0.1, 0.9
        about_button.config(
            command=AboutPage.show,
            **page_styles.about_button,
        )
        about_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            text=i18n.get("menu.about_button"),
            coords=(rel_x, rel_y + 0.06),
            **page_styles.about_button_text,
        )

        # Exit button
        rel_x, rel_y = 0.92, 0.94
        exit_button.config(
            text=i18n.get("menu.exit_button"),
            command=destroy_all_pages,
            **page_styles.exit_button,
        )
        exit_button.place(relx=rel_x, rely=rel_y, anchor="center")
        cls.set_text_at(
            coords=(rel_x, rel_y + 0.04),
            fg=exit_button.cget("fg"),
            **page_styles.exit_button_text,
        )

        cls.set_footer()

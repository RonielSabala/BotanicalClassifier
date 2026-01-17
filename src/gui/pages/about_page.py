import tkinter as tk
from enum import Enum
from typing import Any

from common.constants import (
    ABOUT_ADDRESS_INFO,
    ABOUT_EMAIL_INFO,
    ABOUT_PHONE_INFO,
    ABOUT_SUBTITLE,
)
from common.paths import FAQ_PATH, POLICIES_PATH, TERMS_PATH
from services.about_service import AboutService
from services.i18n_service import i18n

from ..assets.images import APP_ICON_IMAGE, COUNTRY_SHIELD_IMAGE
from ..page import Page
from ..styles import about_page as page_styles
from .menu_page import MenuPage


class PageSymbols(str, Enum):
    ADDRESS = "📍"
    PHONE = "📞"
    EMAIL = "📧"
    LINKS_SEPARATION = "|"


class AboutPage(Page):
    prev_page = MenuPage

    # - Utils:

    @classmethod
    def _set_link_separator(
        cls, *, root: tk.Frame, row: int, column: int, styles: dict[str, Any]
    ) -> None:
        label = cls.get_label(root)
        label.config(text=PageSymbols.LINKS_SEPARATION, padx=0, **styles)
        label.grid(row=row, column=column, sticky="ns")

    # - Overridden methods:

    @classmethod
    def load(cls) -> None:
        # - Page elements:

        header_grid = cls.get_grid()
        content_grid = cls.get_grid()
        links_grid = cls.get_grid()

        shield_image = cls.get_label(header_grid, COUNTRY_SHIELD_IMAGE)
        icon_image = cls.get_label(header_grid, APP_ICON_IMAGE)
        title = cls.get_label(header_grid)
        subtitle = cls.get_label(header_grid)

        address_emoji = cls.get_label(content_grid)
        address_label = cls.get_label(content_grid)
        address_info = cls.get_label(content_grid)

        phone_emoji = cls.get_label(content_grid)
        phone_label = cls.get_label(content_grid)
        phone_info = cls.get_label(content_grid)

        email_emoji = cls.get_label(content_grid)
        email_label = cls.get_label(content_grid)
        email_info = cls.get_label(content_grid)

        terms_link = cls.get_button(links_grid)
        policies_link = cls.get_button(links_grid)
        faq_link = cls.get_button(links_grid)

        # - Elements configuration:

        header_grid.grid_rowconfigure(0, pad=45)
        header_grid.grid_columnconfigure(1, pad=0)

        content_grid.grid_rowconfigure(1, pad=50)
        content_grid.grid_columnconfigure(0, weight=1)
        content_grid.grid_columnconfigure(1, pad=40)

        title.config(text=i18n.get("about.title"), **page_styles.title)
        subtitle.config(text=ABOUT_SUBTITLE, font=page_styles.subtitle_font)

        address_emoji.config(text=PageSymbols.ADDRESS, **page_styles.emoji)
        address_label.config(text=i18n.get("about.address"), **page_styles.label)
        address_info.config(
            text=f"{ABOUT_ADDRESS_INFO}\n{i18n.get('about.address_country')}",
            **page_styles.label_info,
        )

        phone_emoji.config(text=PageSymbols.PHONE, **page_styles.emoji)
        phone_label.config(text=i18n.get("about.phone"), **page_styles.label)
        phone_info.config(text=ABOUT_PHONE_INFO, **page_styles.label_info)

        email_emoji.config(text=PageSymbols.EMAIL, **page_styles.emoji)
        email_label.config(text=i18n.get("about.email"), **page_styles.label)
        email_info.config(text=ABOUT_EMAIL_INFO, **page_styles.label_info)

        terms_link.config(
            text=i18n.get("about.terms.title"),
            command=TermsPage.show,
            **page_styles.link,
        )
        policies_link.config(
            text=i18n.get("about.policies.title"),
            command=PoliciesPage.show,
            **page_styles.link,
        )
        faq_link.config(
            text=i18n.get("about.faq.title"),
            command=FaqPage.show,
            **page_styles.link,
        )

        # - Elements widget arrangement:

        cls.set_return_button()

        # Grids
        header_grid.pack(fill="none", padx=85, pady=40)
        content_grid.pack(fill="none", expand=True, padx=85, pady=35)
        links_grid.pack(fill="y", padx=0, pady=100)

        # Header
        shield_image.grid(row=0, column=0, sticky="nse")
        cls._set_link_separator(
            root=header_grid, row=0, column=1, styles=page_styles.header_separator
        )
        icon_image.grid(row=0, column=2, sticky="nsw")
        title.grid(row=1, columnspan=3, sticky="nsew")
        subtitle.grid(row=2, columnspan=3, pady=6, sticky="nsew")

        # Address
        address_emoji.grid(row=0, column=0, sticky="nsew")
        address_label.grid(row=0, column=1, sticky="nsew")
        address_info.grid(row=0, column=2, sticky="nsew")

        # Phone
        phone_emoji.grid(row=1, column=0, sticky="nsew")
        phone_label.grid(row=1, column=1, sticky="nsew")
        phone_info.grid(row=1, column=2, sticky="nsw")

        # Email
        email_emoji.grid(row=2, column=0, sticky="nse")
        email_label.grid(row=2, column=1, sticky="nsew")
        email_info.grid(row=2, column=2, sticky="nsw")

        # Links
        terms_link.grid(row=0, column=0, sticky="nse")
        cls._set_link_separator(
            root=links_grid, row=0, column=1, styles=page_styles.link_separator
        )
        policies_link.grid(row=0, column=2, sticky="ns")
        cls._set_link_separator(
            root=links_grid, row=0, column=3, styles=page_styles.link_separator
        )
        faq_link.grid(row=0, column=4, sticky="nsw")

        cls.set_copyright()


class FaqPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Page elements
        scrollable_text = cls.get_scrollable_text()

        # Elements configuration
        scrollable_text.insert(tk.END, AboutService.get_page_content(FAQ_PATH))
        scrollable_text.config(state=tk.DISABLED, **page_styles.faq_scrollable_text)

        # - Elements widget configuration:

        cls.set_return_button()

        # Title
        cls.set_empty_separator(pady=35)
        cls.set_text(text=i18n.get("about.faq.title"), **page_styles.title)
        cls.set_empty_separator(pady=25)

        # Scrollable text
        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        cls.set_empty_separator(pady=35)


class PoliciesPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Page elements
        scrollable_text = cls.get_scrollable_text()

        # Elements configuration
        scrollable_text.insert(tk.END, AboutService.get_page_content(POLICIES_PATH))
        scrollable_text.config(state=tk.DISABLED, **page_styles.default_scrollable_text)

        # - Elements widget configuration:

        cls.set_return_button()

        # Title
        cls.set_empty_separator(pady=35)
        cls.set_text(text=i18n.get("about.policies.title"), **page_styles.title)
        cls.set_empty_separator(pady=0)

        # Scrollable text
        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        cls.set_empty_separator(pady=30)


class TermsPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Page elements
        scrollable_text = cls.get_scrollable_text()

        # Elements configuration
        scrollable_text.insert(tk.END, AboutService.get_page_content(TERMS_PATH))
        scrollable_text.config(state=tk.DISABLED, **page_styles.default_scrollable_text)

        # - Elements widget configuration:

        cls.set_return_button()

        # Title
        cls.set_empty_separator(pady=35)
        cls.set_text(text=i18n.get("about.terms.title"), **page_styles.title)
        cls.set_empty_separator(pady=0)

        # Scrollable text
        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        cls.set_empty_separator(pady=30)

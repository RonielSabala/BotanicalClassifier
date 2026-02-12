"""
About-related pages: About, FAQ, Policies, and Terms.
"""

import tkinter as tk
from collections.abc import Callable
from enum import Enum
from typing import Any

from common.constants import ABOUT
from services import AboutService, i18n

from ..assets import APP_ICON_IMAGE, COUNTRY_SHIELD_IMAGE
from ..page import Page
from ..styles import about_page as page_styles
from .menu_page import MenuPage


class UISymbols(str, Enum):
    ADDRESS = "📍"
    PHONE = "📞"
    EMAIL = "📧"
    LINKS_SEPARATION = "|"


class AboutPage(Page):
    """
    Main About page with organization details and links
    to legal/FAQ pages.
    """

    prev_page = MenuPage

    # - UI Helpers:

    @classmethod
    def _add_link_separator(
        cls, *, root: tk.Frame, row: int, column: int, styles: dict[str, Any]
    ) -> None:
        label = cls.get_label(root)
        label.config(text=UISymbols.LINKS_SEPARATION, **styles)
        label.grid(row=row, column=column, sticky="ns")

    # - Overridden methods:

    @classmethod
    def load(cls) -> None:
        # - Widgets:

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

        # - Configuration:

        header_grid.grid_rowconfigure(0, pad=45)
        header_grid.grid_columnconfigure(1, pad=0)

        content_grid.grid_rowconfigure(1, pad=50)
        content_grid.grid_columnconfigure(0, weight=1)
        content_grid.grid_columnconfigure(1, pad=40)

        title.config(text=i18n.get("about.title"), **page_styles.title)
        subtitle.config(text=ABOUT.subtitle, font=page_styles.subtitle_font)

        address_emoji.config(text=UISymbols.ADDRESS, **page_styles.emoji)
        address_label.config(text=i18n.get("about.address"), **page_styles.label)
        address_info.config(
            text=f"{ABOUT.address}\n{i18n.get('about.address_country')}",
            **page_styles.label_info,
        )

        phone_emoji.config(text=UISymbols.PHONE, **page_styles.emoji)
        phone_label.config(text=i18n.get("about.phone"), **page_styles.label)
        phone_info.config(text=ABOUT.address, **page_styles.label_info)

        email_emoji.config(text=UISymbols.EMAIL, **page_styles.emoji)
        email_label.config(text=i18n.get("about.email"), **page_styles.label)
        email_info.config(text=ABOUT.email, **page_styles.label_info)

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
            text=i18n.get("about.faq.title"), command=FaqPage.show, **page_styles.link
        )

        # - Layout:

        cls.set_return_button()

        # Grids
        header_grid.pack(fill="none", padx=85, pady=40)
        content_grid.pack(fill="none", expand=True, padx=85, pady=35)
        links_grid.pack(fill="y", pady=100)

        # Header
        shield_image.grid(row=0, column=0, sticky="nse")
        cls._add_link_separator(
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
        cls._add_link_separator(
            root=links_grid, row=0, column=1, styles=page_styles.link_separator
        )
        policies_link.grid(row=0, column=2, sticky="ns")
        cls._add_link_separator(
            root=links_grid, row=0, column=3, styles=page_styles.link_separator
        )
        faq_link.grid(row=0, column=4, sticky="nsw")

        cls.set_copyright()


class _ScrollableTextPage(Page):
    """
    Base class for simple read-only text pages.
    """

    title_key: str
    content_loader: Callable

    title_pad_y: int
    scrollable_text_pad_y: int
    scrollable_text_styles: dict[str, Any]

    @classmethod
    def load(cls) -> None:
        # Widget
        scrollable_text = cls.get_scrollable_text()

        # Configuration
        scrollable_text.insert(tk.END, cls.content_loader())
        scrollable_text.config(state=tk.DISABLED, **cls.scrollable_text_styles)

        # - Layout:

        cls.set_return_button()

        # Title
        cls.set_empty_separator(pady=35)
        cls.set_text(text=i18n.get(cls.title_key), **page_styles.title)
        cls.set_empty_separator(pady=cls.title_pad_y)

        # Scrollable text
        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        cls.set_empty_separator(pady=cls.scrollable_text_pad_y)


class FaqPage(_ScrollableTextPage):
    prev_page = AboutPage
    title_key = "about.faq.title"
    content_loader = AboutService.get_faq
    title_pad_y = 25
    scrollable_text_pad_y = 35
    scrollable_text_styles = page_styles.faq_scrollable_text


class PoliciesPage(_ScrollableTextPage):
    prev_page = AboutPage
    title_key = "about.policies.title"
    content_loader = AboutService.get_policies
    title_pad_y = 0
    scrollable_text_pad_y = 30
    scrollable_text_styles = page_styles.default_scrollable_text


class TermsPage(_ScrollableTextPage):
    prev_page = AboutPage
    title_key = "about.terms.title"
    content_loader = AboutService.get_terms
    title_pad_y = 0
    scrollable_text_pad_y = 30
    scrollable_text_styles = page_styles.default_scrollable_text

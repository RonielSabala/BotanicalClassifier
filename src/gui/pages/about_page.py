import tkinter as tk
from tkinter import Frame, scrolledtext
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
from ..styles.about_page import (
    emoji_style,
    header_separator_style,
    label_info_style,
    label_style,
    link_separator_style,
    link_style,
)
from .menu_page import MenuPage

# GUI defaults
ADDRESS_EMOJI = "📍"
PHONE_EMOJI = "📞"
EMAIL_EMOJI = "📧"
LINKS_SEPARATION_TEXT = "|"


class AboutPage(Page):
    prev_page = MenuPage

    @classmethod
    def _set_link_separator(
        cls, *, root: Frame, row: int, column: int, styles: dict[str, Any]
    ) -> None:
        tk.Label(
            root,
            text=LINKS_SEPARATION_TEXT,
            padx=0,
            bg=cls.bg_color,
            **styles,
        ).grid(row=row, column=column, sticky="ns")

    @classmethod
    def load(cls) -> None:
        bg_color = cls.bg_color

        # - Grids creation:

        header_grid = cls.get_grid_from_root()
        header_grid.pack(fill="none", padx=85, pady=40)
        header_grid.grid_rowconfigure(0, pad=45)
        header_grid.grid_columnconfigure(1, pad=0)

        content_grid = cls.get_grid_from_root()
        content_grid.pack(fill="none", expand=True, padx=85, pady=35)
        content_grid.grid_columnconfigure(0, weight=1)
        content_grid.grid_rowconfigure(1, pad=50)
        content_grid.grid_columnconfigure(1, pad=40)

        links_grid = cls.get_grid_from_root()
        links_grid.pack(fill="y", padx=0, pady=100)

        # - Header elements:

        cls.set_return_btn()
        shield = tk.Label(header_grid, image=COUNTRY_SHIELD_IMAGE, bg=bg_color)
        icon = tk.Label(header_grid, image=APP_ICON_IMAGE, bg=bg_color)

        title = tk.Label(
            header_grid,
            text=i18n.get("about.title"),
            bg=bg_color,
            font=("Arial", 30),
        )

        subtitle = tk.Label(
            header_grid,
            text=ABOUT_SUBTITLE,
            bg=bg_color,
            font=("Arial", 15),
        )

        # - Page content:

        address_emoji = tk.Label(
            content_grid, text=ADDRESS_EMOJI, bg=bg_color, **emoji_style
        )

        address_label = tk.Label(
            content_grid, text=i18n.get("about.address"), bg=bg_color, **label_style
        )

        address_info = tk.Label(
            content_grid,
            text=f"{ABOUT_ADDRESS_INFO}\n{i18n.get('about.address_country')}",
            bg=bg_color,
            **label_info_style,
        )

        phone_emoji = tk.Label(
            content_grid, text=PHONE_EMOJI, bg=bg_color, **emoji_style
        )

        phone_label = tk.Label(
            content_grid, text=i18n.get("about.phone"), bg=bg_color, **label_style
        )

        phone_info = tk.Label(
            content_grid, text=ABOUT_PHONE_INFO, bg=bg_color, **label_info_style
        )

        email_emoji = tk.Label(
            content_grid, text=EMAIL_EMOJI, bg=bg_color, **emoji_style
        )

        email_label = tk.Label(
            content_grid, text=i18n.get("about.email"), bg=bg_color, **label_style
        )

        email_info = tk.Label(
            content_grid, text=ABOUT_EMAIL_INFO, bg=bg_color, **label_info_style
        )

        # - Page links:

        terms_button = tk.Button(
            links_grid,
            text=i18n.get("about.terms.title"),
            command=TermsPage.show,
            bg=bg_color,
            activebackground=bg_color,
            **link_style,
        )

        policies_button = tk.Button(
            links_grid,
            text=i18n.get("about.policies.title"),
            command=PoliciesPage.show,
            bg=bg_color,
            activebackground=bg_color,
            **link_style,
        )

        faq_button = tk.Button(
            links_grid,
            text=i18n.get("about.faq.title"),
            command=FaqPage.show,
            bg=bg_color,
            activebackground=bg_color,
            **link_style,
        )

        # - Elements configuration:

        # Header
        shield.grid(row=0, column=0, sticky="nse")
        cls._set_link_separator(
            root=header_grid, row=0, column=1, styles=header_separator_style
        )

        icon.grid(row=0, column=2, sticky="nsw")
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

        # - Links:

        terms_button.grid(row=0, column=0, sticky="nse")
        cls._set_link_separator(
            root=links_grid, row=0, column=1, styles=link_separator_style
        )

        policies_button.grid(row=0, column=2, sticky="ns")
        cls._set_link_separator(
            root=links_grid, row=0, column=3, styles=link_separator_style
        )

        faq_button.grid(row=0, column=4, sticky="nsw")
        cls.set_footer()


class FaqPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Header
        cls.set_return_btn()
        cls.set_text("", font_size=0, pady=35)
        cls.set_text(i18n.get("about.faq.title"), font_size=30, pady=0, fg="#091518")
        cls.set_text("", font_size=0, pady=25)

        # Content
        scrollable_text = scrolledtext.ScrolledText(
            cls.root, wrap=tk.WORD, width=50, height=12
        )

        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        scrollable_text.config(state=tk.NORMAL, font=("Arial", 13), relief="flat")
        scrollable_text.insert(tk.END, AboutService.get_page_content(FAQ_PATH))
        scrollable_text.config(state=tk.DISABLED)
        cls.set_text("", font_size=0, pady=35)


class PoliciesPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Header
        cls.set_return_btn()
        cls.set_text("", font_size=0, pady=35)
        cls.set_text(
            i18n.get("about.policies.title"), font_size=30, pady=0, fg="#091518"
        )

        cls.set_text("", font_size=0, pady=0)

        # Content
        scrollable_text = scrolledtext.ScrolledText(
            cls.root, wrap=tk.WORD, width=50, height=12
        )

        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        scrollable_text.config(state=tk.NORMAL, font=("Arial", 10), bg="Gray95")
        scrollable_text.insert(tk.END, AboutService.get_page_content(POLICIES_PATH))
        scrollable_text.config(state=tk.DISABLED)
        cls.set_text("", font_size=0, pady=30)


class TermsPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Header
        cls.set_return_btn()
        cls.set_text("", font_size=0, pady=35)
        cls.set_text(i18n.get("about.terms.title"), font_size=30, pady=0, fg="#091518")
        cls.set_text("", font_size=0, pady=0)

        # Content
        scrollable_text = scrolledtext.ScrolledText(
            cls.root, wrap=tk.WORD, width=50, height=12
        )

        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        scrollable_text.config(state=tk.NORMAL, font=("Arial", 10), bg="Gray95")
        scrollable_text.insert(tk.END, AboutService.get_page_content(TERMS_PATH))
        scrollable_text.config(state=tk.DISABLED)
        cls.set_text("", font_size=0, pady=30)

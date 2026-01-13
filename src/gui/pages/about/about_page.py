import tkinter as tk
from tkinter import Frame

from common.i18n import i18n

from ...assets.loaded_images import APP_ICON_IMAGE, COUNTRY_SHIELD_IMAGE
from ...styles import (
    list_emoji_style,
    list_info_style,
    list_link_style,
    list_title_style,
)
from ..menu_page import MenuPage
from ..page import Page

LOCATION_EMOJI = "📍"
PHONE_EMOJI = "📞"
EMAIL_EMOJI = "📧"
PHONE_INFO = "(809) 385-2611 Ext. 221"
EMAIL_INFO = "jardinbotanico@jbn.gob.do"
PAGE_SUBTITLE = "Dr. Rafael M. Moscoso"


class AboutPage(Page):
    prev_page = MenuPage

    @classmethod
    def get_separation(cls, frame: Frame, font_size: int):
        return tk.Label(
            frame,
            text="|",
            font=("Arial", font_size),
            fg="Gray20",
            bg=cls.bg_color,
            padx=0,
        )

    @classmethod
    def load(cls) -> None:
        from ._faq_page import FaqPage
        from ._policies_page import PoliciesPage
        from ._terms_page import TermsPage

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
        shield = tk.Label(header_grid, image=COUNTRY_SHIELD_IMAGE, bg=cls.bg_color)
        icon = tk.Label(header_grid, image=APP_ICON_IMAGE, bg=cls.bg_color)

        title = tk.Label(
            header_grid,
            text=i18n.get("about.title"),
            font=("Arial", 30),
            bg=cls.bg_color,
        )

        subtitle = tk.Label(
            header_grid,
            text=PAGE_SUBTITLE,
            font=("Arial", 15),
            bg=cls.bg_color,
        )

        # - Page content:

        location_emoji = tk.Label(content_grid, text=LOCATION_EMOJI, **list_emoji_style)
        location_label = tk.Label(
            content_grid, text=i18n.get("about.location"), **list_title_style
        )

        location_info = tk.Label(
            content_grid, text=i18n.get("about.location_info"), **list_info_style
        )

        phone_emoji = tk.Label(content_grid, text=PHONE_EMOJI, **list_emoji_style)
        phone_label = tk.Label(
            content_grid, text=i18n.get("about.phone"), **list_title_style
        )

        phone_info = tk.Label(content_grid, text=PHONE_INFO, **list_info_style)

        email_emoji = tk.Label(content_grid, text=EMAIL_EMOJI, **list_emoji_style)
        email_label = tk.Label(
            content_grid, text=i18n.get("about.email"), **list_title_style
        )

        email_info = tk.Label(content_grid, text=EMAIL_INFO, **list_info_style)

        # - Page links:

        terms_button = tk.Button(
            links_grid,
            text=i18n.get("about.terms.title"),
            command=TermsPage.show,
            **list_link_style,
        )

        policies_button = tk.Button(
            links_grid,
            text=i18n.get("about.policies.title"),
            command=PoliciesPage.show,
            **list_link_style,
        )

        faq_button = tk.Button(
            links_grid,
            text=i18n.get("about.faq.title"),
            command=FaqPage.show,
            **list_link_style,
        )

        # - Elements configuration:

        # Header
        shield.grid(row=0, column=0, sticky="nse")
        header_separator = cls.get_separation(header_grid, 25)
        header_separator.grid(row=0, column=1, sticky="ns")
        icon.grid(row=0, column=2, sticky="nsw")
        title.grid(row=1, columnspan=3, sticky="nsew")
        subtitle.grid(row=2, columnspan=3, sticky="nsew", pady=6)

        # Location
        location_emoji.grid(row=0, column=0, sticky="nsew")
        location_label.grid(row=0, column=1, sticky="nsew")
        location_info.grid(row=0, column=2, sticky="nsew")

        # Phone
        phone_emoji.grid(row=1, column=0, sticky="nsew")
        phone_label.grid(row=1, column=1, sticky="nsew")
        phone_info.grid(row=1, column=2, sticky="nsw")

        # Email
        email_emoji.grid(row=2, column=0, sticky="nse")
        email_label.grid(row=2, column=1, sticky="nsew")
        email_info.grid(row=2, column=2, sticky="nsw")

        # Links
        terms_button.grid(row=0, column=0, sticky="nse")
        terms_separator = cls.get_separation(links_grid, 16)
        terms_separator.grid(row=0, column=1, sticky="ns")
        policies_button.grid(row=0, column=2, sticky="ns")
        policies_separator = cls.get_separation(links_grid, 16)
        policies_separator.grid(row=0, column=3, sticky="ns")
        faq_button.grid(row=0, column=4, sticky="nsw")

        cls.set_footer()

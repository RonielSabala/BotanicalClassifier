import tkinter as tk

from ...assets.images import ICON_IMG, SHIELD_IMG
from ...styles import list_icon, list_info, list_link, list_title
from ..menu_page import Menu
from ..page import Page

# Page title and subtitle
PAGE_TITLE = "Jardín Botánico Nacional"
PAGE_SUBTITLE = "Dr. Rafael M. Moscoso"

# Organization info
ORG_PHONE = "(809) 385-2611 Ext. 221"
ORG_EMAIL = "jardinbotanico@jbn.gob.do"
ORG_LOCATION = """Av. República de Colombia esq. Av. Los Próceres
Sector los Altos de Galá, Santo Domingo, D.N
República Dominicana"""


class Contact(Page):
    prev_page = Menu

    @classmethod
    def get_separation(cls, frame, font_size: int):
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
        from ._faq import Faq
        from ._policies import Policies
        from ._terms import Terms

        # Create grids
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

        # Header
        cls.set_return_btn()
        shield = tk.Label(header_grid, image=SHIELD_IMG, bg=cls.bg_color)
        sep_header = cls.get_separation(header_grid, 25)
        icon = tk.Label(header_grid, image=ICON_IMG, bg=cls.bg_color)
        title = tk.Label(
            header_grid, text=PAGE_TITLE, font=("Arial", 30), bg=cls.bg_color
        )

        subtitle = tk.Label(
            header_grid, text=PAGE_SUBTITLE, font=("Arial", 15), bg=cls.bg_color
        )

        # Page content
        location = tk.Label(content_grid, text="📍", **list_icon)
        location_text = tk.Label(content_grid, text="Dirección", **list_title)
        location_info = tk.Label(content_grid, text=ORG_LOCATION, **list_info)

        phone = tk.Label(content_grid, text="📞", **list_icon)
        phone_text = tk.Label(content_grid, text="Tel.", **list_title)
        phone_info = tk.Label(content_grid, text=ORG_PHONE, **list_info)

        email = tk.Label(content_grid, text="📧", **list_icon)
        email_text = tk.Label(content_grid, text="Email", **list_title)
        email_info = tk.Label(content_grid, text=ORG_EMAIL, **list_info)

        # Links
        terms = tk.Button(
            links_grid,
            text="Términos De Uso",
            command=Terms.show,
            **list_link,
        )

        policies = tk.Button(
            links_grid,
            text="Políticas De Privacidad",
            command=Policies.show,
            **list_link,
        )

        faq = tk.Button(
            links_grid,
            text="Preguntas Frecuentes",
            command=Faq.show,
            **list_link,
        )

        # - Elements config:

        # Title and subtitle
        shield.grid(row=0, column=0, sticky="nse")
        sep_header.grid(row=0, column=1, sticky="ns")
        icon.grid(row=0, column=2, sticky="nsw")
        title.grid(row=1, columnspan=3, sticky="nsew")
        subtitle.grid(row=2, columnspan=3, sticky="nsew", pady=6)

        # Location
        location.grid(row=0, column=0, sticky="nsew")
        location_text.grid(row=0, column=1, sticky="nsew")
        location_info.grid(row=0, column=2, sticky="nsew")

        # Phone
        phone.grid(row=1, column=0, sticky="nsew")
        phone_text.grid(row=1, column=1, sticky="nsew")
        phone_info.grid(row=1, column=2, sticky="nsw")

        # Email
        email.grid(row=2, column=0, sticky="nse")
        email_text.grid(row=2, column=1, sticky="nsew")
        email_info.grid(row=2, column=2, sticky="nsw")

        # Links
        sep1 = cls.get_separation(links_grid, 16)
        sep2 = cls.get_separation(links_grid, 16)
        terms.grid(row=0, column=0, sticky="nse")
        sep1.grid(row=0, column=1, sticky="ns")
        policies.grid(row=0, column=2, sticky="ns")
        sep2.grid(row=0, column=3, sticky="ns")
        faq.grid(row=0, column=4, sticky="nsw")

        cls.set_footer()

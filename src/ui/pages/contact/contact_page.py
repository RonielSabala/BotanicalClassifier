import tkinter as tk

from ...assets.main import ICON_IMG, SHIELD_IMG
from ...styles import list_icono, list_info, list_link, list_titulo
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
    pagina_anterior = Menu

    @classmethod
    def obtener_sep(cls, frame, tamaño: int):
        return tk.Label(
            frame,
            text="|",
            font=("Arial", tamaño),
            fg="Gray20",
            bg=cls.color_fondo,
            padx=0,
        )

    @classmethod
    def load(cls) -> None:
        from ._faq import Faq
        from ._policies import Policies
        from ._terms import Terms

        # Create grids
        grid_header = cls.get_grid()
        grid_header.pack(fill="none", padx=85, pady=40)
        grid_header.grid_rowconfigure(0, pad=45)
        grid_header.grid_columnconfigure(1, pad=0)

        grid = cls.get_grid()
        grid.pack(fill="none", expand=True, padx=85, pady=35)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_rowconfigure(1, pad=50)
        grid.grid_columnconfigure(1, pad=40)

        grid_links = cls.get_grid()
        grid_links.pack(fill="y", padx=0, pady=100)

        # Title and subtitle
        cls.set_return_btn()
        shield = tk.Label(grid_header, image=SHIELD_IMG, bg=cls.color_fondo)
        sep_header = cls.obtener_sep(grid_header, 25)
        icon = tk.Label(grid_header, image=ICON_IMG, bg=cls.color_fondo)
        title = tk.Label(
            grid_header, text=PAGE_TITLE, font=("Arial", 30), bg=cls.color_fondo
        )

        subtitle = tk.Label(
            grid_header, text=PAGE_SUBTITLE, font=("Arial", 15), bg=cls.color_fondo
        )

        # Page content
        location = tk.Label(grid, text="📍", **list_icono)
        location_text = tk.Label(grid, text="Dirección", **list_titulo)
        location_info = tk.Label(grid, text=ORG_LOCATION, **list_info)

        phone = tk.Label(grid, text="📞", **list_icono)
        phone_text = tk.Label(grid, text="Tel.", **list_titulo)
        phone_info = tk.Label(grid, text=ORG_PHONE, **list_info)

        email = tk.Label(grid, text="📧", **list_icono)
        email_text = tk.Label(grid, text="Email", **list_titulo)
        email_info = tk.Label(grid, text=ORG_EMAIL, **list_info)

        # Links
        terms = tk.Button(
            grid_links,
            text="Términos De Uso",
            command=Terms.show,
            **list_link,
        )

        policies = tk.Button(
            grid_links,
            text="Políticas De Privacidad",
            command=Policies.show,
            **list_link,
        )

        faq = tk.Button(
            grid_links,
            text="Preguntas Frecuentes",
            command=Faq.show,
            **list_link,
        )

        # Links separators
        sep1 = cls.obtener_sep(grid_links, 16)
        sep2 = cls.obtener_sep(grid_links, 16)

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
        terms.grid(row=0, column=0, sticky="nse")
        sep1.grid(row=0, column=1, sticky="ns")
        policies.grid(row=0, column=2, sticky="ns")
        sep2.grid(row=0, column=3, sticky="ns")
        faq.grid(row=0, column=4, sticky="nsw")

        cls.set_footer()

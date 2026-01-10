import tkinter as tk

from ...assets.main import ICON_IMG, SHIELD_IMG
from ...main import Page
from ...styles import main as Estilos
from ..menu.main import Menu

# Page text
PAGE_TITLE = "Jardín Botánico Nacional"
PAGE_SUBTITLE = "Dr. Rafael M. Moscoso"

# Organization info
ORG_EMAIL = "jardinbotanico@jbn.gob.do"
ORG_PHONE_NUMBER = "(809) 385-2611 Ext. 221"
ORG_DIRECTION = """Av. República de Colombia esq. Av. Los Próceres
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
    def cargar(cls) -> None:
        from ._faq import Faq
        from ._policies import Policies
        from ._terms import Terms

        # - Creación de los grids:

        grid_header = cls.obtener_grid()
        grid_header.pack(fill="none", padx=85, pady=40)
        grid_header.grid_rowconfigure(0, pad=45)
        grid_header.grid_columnconfigure(1, pad=0)

        grid = cls.obtener_grid()
        grid.pack(fill="none", expand=True, padx=85, pady=35)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_rowconfigure(1, pad=50)
        grid.grid_columnconfigure(1, pad=40)

        grid_links = cls.obtener_grid()
        grid_links.pack(fill="y", padx=0, pady=100)

        # - Header:

        cls.colocar_retorno()
        escudo = tk.Label(grid_header, image=SHIELD_IMG, bg=cls.color_fondo)
        sep_header = cls.obtener_sep(grid_header, 25)
        icono = tk.Label(grid_header, image=ICON_IMG, bg=cls.color_fondo)
        titulo = tk.Label(
            grid_header, text=PAGE_TITLE, font=("Arial", 30), bg=cls.color_fondo
        )

        sub_titulo = tk.Label(
            grid_header, text=PAGE_SUBTITLE, font=("Arial", 15), bg=cls.color_fondo
        )

        # - Contenido:

        direccion = tk.Label(grid, text="📍", **Estilos.list_icono)
        texto_direccion = tk.Label(grid, text="Dirección", **Estilos.list_titulo)
        info_direccion = tk.Label(grid, text=ORG_DIRECTION, **Estilos.list_info)

        telefono = tk.Label(grid, text="📞", **Estilos.list_icono)
        texto_telefono = tk.Label(grid, text="Tel.", **Estilos.list_titulo)
        info_telefono = tk.Label(grid, text=ORG_PHONE_NUMBER, **Estilos.list_info)

        email = tk.Label(grid, text="📧", **Estilos.list_icono)
        texto_email = tk.Label(grid, text="Email", **Estilos.list_titulo)
        info_email = tk.Label(grid, text=ORG_EMAIL, **Estilos.list_info)

        # - Links:

        terminos = tk.Button(
            grid_links,
            text="Términos De Uso",
            command=Terms.mostrar,
            **Estilos.list_link,
        )

        politicas = tk.Button(
            grid_links,
            text="Políticas De Privacidad",
            command=Policies.mostrar,
            **Estilos.list_link,
        )

        preguntas = tk.Button(
            grid_links,
            text="Preguntas Frecuentes",
            command=Faq.mostrar,
            **Estilos.list_link,
        )

        # Separadores para los links
        sep1 = cls.obtener_sep(grid_links, 16)
        sep2 = cls.obtener_sep(grid_links, 16)

        # - Configuración:

        # Header
        escudo.grid(row=0, column=0, sticky="nse")
        sep_header.grid(row=0, column=1, sticky="ns")
        icono.grid(row=0, column=2, sticky="nsw")
        titulo.grid(row=1, columnspan=3, sticky="nsew")
        sub_titulo.grid(row=2, columnspan=3, sticky="nsew", pady=6)

        # Dirección
        direccion.grid(row=0, column=0, sticky="nsew")
        texto_direccion.grid(row=0, column=1, sticky="nsew")
        info_direccion.grid(row=0, column=2, sticky="nsew")

        # Teléfono
        telefono.grid(row=1, column=0, sticky="nsew")
        texto_telefono.grid(row=1, column=1, sticky="nsew")
        info_telefono.grid(row=1, column=2, sticky="nsw")

        # Email
        email.grid(row=2, column=0, sticky="nse")
        texto_email.grid(row=2, column=1, sticky="nsew")
        info_email.grid(row=2, column=2, sticky="nsw")

        # Links
        terminos.grid(row=0, column=0, sticky="nse")
        sep1.grid(row=0, column=1, sticky="ns")
        politicas.grid(row=0, column=2, sticky="ns")
        sep2.grid(row=0, column=3, sticky="ns")
        preguntas.grid(row=0, column=4, sticky="nsw")

        cls.colocar_footer()

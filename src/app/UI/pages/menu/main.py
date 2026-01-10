import tkinter as tk
from tkinter import font

from ...assets.main import IMG_BANNER
from ...main import RAIZ, Page, close_pages
from ...styles import main as Estilos


class Menu(Page):
    @classmethod
    def mostrar(cls) -> None:
        cls.configurar_escenas()
        super().mostrar()

    @classmethod
    def cerrar(cls) -> None:
        RAIZ.destroy()

    @classmethod
    def configurar_escenas(cls):
        from ..formulario.main import Formulario

        Formulario.pagina_anterior = cls

    @classmethod
    def cargar(cls) -> None:
        from ..contacto.main import Contact
        from ..formulario.main import Formulario
        from ..tabla.main import Tabla

        # - Header:

        tk.Label(cls.raiz, image=IMG_BANNER, bg=cls.color_fondo).pack(padx=10, pady=5)
        cls.colocar_textoXY(
            "Presidencia de la República: www.presidencia.gob.do",
            9,
            (0.5, 0.01),
            anchor="center",
            fg="black",
        )
        cls.colocar_texto("Flor survey", 35, pady=10, fg="#091518")
        cls.colocar_texto(
            "Estamos realizando una investigación a nivel nacional para calcular\n"
            + "la cantidad de flores de cada tipo que tienen las personas en sus\n"
            + "hogares.",
            12,
            pady=25,
            fg="#091518",
        )
        cls.colocar_texto("_" * 70, 10, pady=0, fg="#091518")
        cls.colocar_texto(
            "¿Te gustaría participar?",
            15,
            pady=25,
            fg="#091518",
        )
        cls.colocar_texto(
            "Solo tienes que completar la siguiente encuesta:",
            13,
            pady=3,
            fg="#091518",
        )
        cls.colocar_texto("", 13, pady=15, fg="#091518")

        # - Creación de los botones:

        btn_formulario = tk.Button(
            cls.raiz,
            text="Llenar encuesta",
            command=Formulario.mostrar,
            **Estilos.btn_primario,
        )
        btn_registros = tk.Button(
            cls.raiz,
            text="📝",
            command=Tabla.mostrar,
            fg="ivory4",
            activeforeground="Gray20",
            **Estilos.btn_menu,
        )
        btn_sobre_nosotros = tk.Button(
            cls.raiz,
            text="❀",
            command=Contact.mostrar,
            fg="springGreen4",
            activeforeground="violetred4",
            **Estilos.btn_menu,
        )
        btn_salir = tk.Button(
            cls.raiz,
            text="Salir",
            command=close_pages,
            fg="Red3",
            activeforeground="black",
            relief="sunken",
            **Estilos.btn_menu,
        )

        # - Configuración:

        btn_formulario.pack(pady=0)

        # Botón de registros
        x, y = 0.5, 0.73
        btn_registros.place(relx=x, rely=y, anchor="center")
        cls.colocar_textoXY(
            "Registros", 14, (x - 0.01, y + 0.06), anchor="center", fg="black"
        )

        # Botón sobre nosotros
        x, y = 0.1, 0.9
        btn_sobre_nosotros.place(relx=x, rely=y, anchor="center")
        cls.colocar_textoXY(
            "Sobre\nnosotros", 14, (x, y + 0.06), anchor="center", fg="black"
        )

        # Botón de salir
        x, y = 0.92, 0.94
        btn_salir.config(
            font=font.Font(family="Arial", size=18, underline=True), width=3
        )
        btn_salir.place(relx=x, rely=y, anchor="center")
        cls.colocar_textoXY(
            "⥱", 25, (x, y + 0.04), anchor="center", fg=btn_salir.cget("fg")
        )

        # - Footer:

        cls.colocar_footer()

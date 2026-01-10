import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from common.constants import DEFAULT_IMG
from storage import main as Data

from ...assets.main import IMG_ICONO
from ...main import Page
from ...styles import main as Estilos
from ..menu.main import Menu
from .validaciones import (
    validar_apellido,
    validar_imagen,
    validar_nombre,
    validar_ubicacion,
)


def guardar_formulario() -> None:
    """
    Guarda y valida la información del formulario.
    """

    nombre = Formulario.nombre.get()
    apellido = Formulario.apellido.get()
    ubicacion = Formulario.ubicacion.get()
    imagen = Formulario._imagen

    # Validar campos
    if not (
        validar_nombre(nombre)
        and validar_apellido(apellido)
        and validar_ubicacion(ubicacion)
        and validar_imagen(imagen)
    ):
        return

    try:
        extension = imagen.split(".")[-1]
        ruta = Data.obtener_ruta(f"flor_survey_{Data.n_archivos()}.{extension}")
        Data.agregar_registro(str([nombre, apellido, ubicacion, ruta, None]))
        shutil.copy(imagen, ruta)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Se produjo el siguiente error al guardar el formulario: {e}",
        )

        return

    # Mostrar la pagina anterior
    if pagina := Formulario.pagina_anterior:
        pagina.mostrar()


class Formulario(Page):
    pagina_anterior = Menu

    # Variables
    nombre = tk.StringVar()
    apellido = tk.StringVar()
    ubicacion = tk.StringVar()
    imagen = tk.StringVar()
    _imagen = ""

    @classmethod
    def mostrar(cls) -> None:
        # Restablecer variables
        cls._imagen = ""
        cls.nombre.set("")
        cls.apellido.set("")
        cls.ubicacion.set("")
        cls.imagen.set(DEFAULT_IMG)
        super().mostrar()

    @classmethod
    def cargar(cls) -> None:
        # - Header:

        cls.colocar_retorno()
        tk.Label(cls.raiz, image=IMG_ICONO, bg=cls.color_fondo).pack(padx=10, pady=15)
        cls.colocar_texto("Formulario", 35, pady=15, fg="#091518")
        cls.colocar_texto("", 0, pady=15)

        # - Creación de los campos y botones:

        tamaño = 22
        color = "Black"
        campo_nombre = tk.Entry(
            cls.raiz,
            textvariable=cls.nombre,
            **Estilos.campo_txt,
        )
        campo_apellido = tk.Entry(
            cls.raiz,
            textvariable=cls.apellido,
            **Estilos.campo_txt,
        )
        campo_ubicacion = tk.Entry(
            cls.raiz,
            textvariable=cls.ubicacion,
            **Estilos.campo_txt,
        )
        campo_imagen = tk.Entry(
            cls.raiz,
            textvariable=cls.imagen,
            cursor="hand2",
            state="readonly",
            **Estilos.campo_txt,
        )
        btn_guardar = tk.Button(
            cls.raiz,
            text="Guardar",
            command=lambda: guardar_formulario(),
            **Estilos.btn_primario,
        )

        # - Configuración:

        # Campo principal
        cls.main_element = campo_nombre

        # Campo de usuario
        cls.colocar_texto("Nombre", tamaño, fg=color)
        campo_nombre.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_nombre.bind("<Down>", lambda event: campo_apellido.focus_set())
        campo_nombre.bind("<Return>", lambda event: campo_apellido.focus_set())
        campo_nombre.pack()

        # Campo de apellido
        cls.colocar_texto("", 2)
        cls.colocar_texto("Apellido", tamaño, fg=color)
        campo_apellido.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_apellido.bind("<Up>", lambda event: campo_nombre.focus_set())
        campo_apellido.bind("<Down>", lambda event: campo_ubicacion.focus_set())
        campo_apellido.bind("<Return>", lambda event: campo_ubicacion.focus_set())
        campo_apellido.pack()

        # Campo de ubicación
        cls.colocar_texto("", 2)
        cls.colocar_texto("Ubicación", tamaño, fg=color)
        campo_ubicacion.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_ubicacion.bind("<Up>", lambda event: campo_apellido.focus_set())
        campo_ubicacion.pack()

        # - Campo de imagen:

        def seleccionar_imagen():
            cls._imagen = filedialog.askopenfilename(
                title="Selecciona una imagen",
                filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")],
            )

            if not cls._imagen:
                return

            campo_imagen.config(state="normal")
            campo_imagen.delete(0, tk.END)
            campo_imagen.insert(0, cls._imagen.split("/")[-1])
            campo_imagen.config(state="readonly")

        cls.colocar_texto("", 2)
        cls.colocar_texto("Imagen", tamaño, fg=color)
        campo_imagen.bind("<Button-1>", lambda event: seleccionar_imagen())
        campo_imagen.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_imagen.bind("<Up>", lambda event: campo_ubicacion.focus_set())
        campo_imagen.bind("<Return>", lambda event: btn_guardar.invoke())
        campo_imagen.pack(padx=10, pady=10)
        btn_guardar.pack(pady=40)

        # - Footer:

        cls.colocar_footer()

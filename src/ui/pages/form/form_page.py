import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from common.constants import DEFAULT_IMG_SELECT_STR
from local_storage import main as Data

from ...assets.main import ICON_IMG
from ...styles import btn_primario, campo_txt
from ..menu_page import Menu
from ..page import Page
from .validations import (
    is_valid_image_route,
    is_valid_last_name,
    is_valid_location,
    is_valid_name,
)

# File dialog constants
FILE_DIALOG_TITLE = "Selecciona una imagen"
VALID_FILE_TYPES = [("Archivos de imagen", "*.png;*.jpg;*.jpeg")]


def save_form() -> None:
    """
    Guarda y valida la información del formulario.
    """

    name = Form.name.get()
    last_name = Form.last_name.get()
    location = Form.location.get()
    img = Form._img

    # Validate fields
    if not (
        is_valid_name(name)
        and is_valid_last_name(last_name)
        and is_valid_location(location)
        and is_valid_image_route(img)
    ):
        return

    try:
        img_extension = img.split(".")[-1]
        img_route = Data.obtener_ruta(
            f"flor_survey_{Data.n_archivos()}.{img_extension}"
        )

        Data.agregar_registro(str([name, last_name, location, img_route, None]))
        shutil.copy(img, img_route)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Se produjo el siguiente error al guardar el formulario: {e}",
        )

        return

    # Mostrar la pagina anterior
    if last_page := Form.pagina_anterior:
        last_page.show()


class Form(Page):
    pagina_anterior = Menu

    # Variables
    name = tk.StringVar()
    last_name = tk.StringVar()
    location = tk.StringVar()
    img = tk.StringVar()
    _img = ""

    @classmethod
    def show(cls) -> None:
        # Reset variables
        cls._img = ""
        cls.name.set("")
        cls.last_name.set("")
        cls.location.set("")
        cls.img.set(DEFAULT_IMG_SELECT_STR)
        super().show()

    @classmethod
    def load(cls) -> None:
        # Header
        cls.set_return_btn()
        tk.Label(cls.raiz, image=ICON_IMG, bg=cls.color_fondo).pack(padx=10, pady=15)
        cls.set_text("Formulario", 35, pady=15, fg="#091518")
        cls.set_text("", 0, pady=15)

        # Creación de los campos y botones
        tamaño = 22
        color = "Black"
        campo_nombre = tk.Entry(cls.raiz, textvariable=cls.name, **campo_txt)
        campo_apellido = tk.Entry(cls.raiz, textvariable=cls.last_name, **campo_txt)
        campo_ubicacion = tk.Entry(cls.raiz, textvariable=cls.location, **campo_txt)
        campo_imagen = tk.Entry(
            cls.raiz,
            textvariable=cls.img,
            cursor="hand2",
            state="readonly",
            **campo_txt,
        )

        btn_guardar = tk.Button(
            cls.raiz, text="Guardar", command=lambda: save_form(), **btn_primario
        )

        # - Configuración:

        # Campo principal
        cls.main_element = campo_nombre

        # Campo de usuario
        cls.set_text("Nombre", tamaño, fg=color)
        campo_nombre.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_nombre.bind("<Down>", lambda event: campo_apellido.focus_set())
        campo_nombre.bind("<Return>", lambda event: campo_apellido.focus_set())
        campo_nombre.pack()

        # Campo de apellido
        cls.set_text("", 2)
        cls.set_text("Apellido", tamaño, fg=color)
        campo_apellido.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_apellido.bind("<Up>", lambda event: campo_nombre.focus_set())
        campo_apellido.bind("<Down>", lambda event: campo_ubicacion.focus_set())
        campo_apellido.bind("<Return>", lambda event: campo_ubicacion.focus_set())
        campo_apellido.pack()

        # Campo de ubicación
        cls.set_text("", 2)
        cls.set_text("Ubicación", tamaño, fg=color)
        campo_ubicacion.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_ubicacion.bind("<Up>", lambda event: campo_apellido.focus_set())
        campo_ubicacion.pack()

        # - Campo de imagen:

        def seleccionar_imagen():
            cls._img = filedialog.askopenfilename(
                title=FILE_DIALOG_TITLE,
                filetypes=VALID_FILE_TYPES,
            )

            if not cls._img:
                return

            campo_imagen.config(state="normal")
            campo_imagen.delete(0, tk.END)
            campo_imagen.insert(0, cls._img.split("/")[-1])
            campo_imagen.config(state="readonly")

        cls.set_text("", 2)
        cls.set_text("Imagen", tamaño, fg=color)
        campo_imagen.bind("<Button-1>", lambda event: seleccionar_imagen())
        campo_imagen.bind("<Escape>", lambda event: cls.raiz.focus_set())
        campo_imagen.bind("<Up>", lambda event: campo_ubicacion.focus_set())
        campo_imagen.bind("<Return>", lambda event: btn_guardar.invoke())
        campo_imagen.pack(padx=10, pady=10)
        btn_guardar.pack(pady=40)

        cls.set_footer()

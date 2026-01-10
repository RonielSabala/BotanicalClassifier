import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from common.constants import DEFAULT_IMG_SELECT_STR
from common.utils import get_img_route

from ...assets.images import ICON_IMG
from ...styles import btn_primary, field_text
from ..menu_page import MenuPage
from ..page import Page
from .utils import (
    append_record,
    get_images_count,
    is_valid_image_route,
    is_valid_last_name,
    is_valid_location,
    is_valid_name,
)

# Field constants
FIELD_FONT_SIZE = 22
FIELD_FG_COLOR = "Black"

# File dialog constants
FILE_DIALOG_TITLE = "Selecciona una imagen"
VALID_FILE_TYPES = [("Archivos de imagen", "*.png;*.jpg;*.jpeg")]


def save_form() -> None:
    """
    Guarda y valida la información del formulario.
    """

    name = FormPage.name.get()
    last_name = FormPage.last_name.get()
    location = FormPage.location.get()
    img = FormPage._img

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
        img_route = get_img_route(f"flor_survey_{get_images_count()}.{img_extension}")

        append_record(str([name, last_name, location, img_route, None]))
        shutil.copy(img, img_route)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Se produjo el siguiente error al guardar el formulario: {e}",
        )

        return

    # Show previous page
    if FormPage.prev_page is not None:
        FormPage.prev_page.show()


class FormPage(Page):
    prev_page = MenuPage

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
        tk.Label(cls.root, image=ICON_IMG, bg=cls.bg_color).pack(padx=10, pady=15)
        cls.set_text("Formulario", 35, pady=15, fg="#091518")
        cls.set_text("", 0, pady=15)

        # Create fields and buttons
        name_field = tk.Entry(cls.root, textvariable=cls.name, **field_text)
        last_name_field = tk.Entry(cls.root, textvariable=cls.last_name, **field_text)
        location_field = tk.Entry(cls.root, textvariable=cls.location, **field_text)
        img_field = tk.Entry(
            cls.root,
            textvariable=cls.img,
            cursor="hand2",
            state="readonly",
            **field_text,
        )

        btn_save = tk.Button(
            cls.root, text="Guardar", command=lambda: save_form(), **btn_primary
        )

        # - Configure elements:

        cls.main_field = name_field

        # Name field
        cls.set_text("Nombre", FIELD_FONT_SIZE, fg=FIELD_FG_COLOR)
        name_field.bind("<Escape>", lambda event: cls.root.focus_set())
        name_field.bind("<Down>", lambda event: last_name_field.focus_set())
        name_field.bind("<Return>", lambda event: last_name_field.focus_set())
        name_field.pack()

        # Last name field
        cls.set_text("", 2)
        cls.set_text("Apellido", FIELD_FONT_SIZE, fg=FIELD_FG_COLOR)
        last_name_field.bind("<Escape>", lambda event: cls.root.focus_set())
        last_name_field.bind("<Up>", lambda event: name_field.focus_set())
        last_name_field.bind("<Down>", lambda event: location_field.focus_set())
        last_name_field.bind("<Return>", lambda event: location_field.focus_set())
        last_name_field.pack()

        # Location field
        cls.set_text("", 2)
        cls.set_text("Ubicación", FIELD_FONT_SIZE, fg=FIELD_FG_COLOR)
        location_field.bind("<Escape>", lambda event: cls.root.focus_set())
        location_field.bind("<Up>", lambda event: last_name_field.focus_set())
        location_field.pack()

        # - Image field:

        def ask_select_image():
            cls._img = filedialog.askopenfilename(
                title=FILE_DIALOG_TITLE,
                filetypes=VALID_FILE_TYPES,
            )

            if not cls._img:
                return

            img_field.config(state="normal")
            img_field.delete(0, tk.END)
            img_field.insert(0, cls._img.split("/")[-1])
            img_field.config(state="readonly")

        cls.set_text("", 2)
        cls.set_text("Imagen", FIELD_FONT_SIZE, fg=FIELD_FG_COLOR)
        img_field.bind("<Button-1>", lambda event: ask_select_image())
        img_field.bind("<Escape>", lambda event: cls.root.focus_set())
        img_field.bind("<Up>", lambda event: location_field.focus_set())
        img_field.bind("<Return>", lambda event: btn_save.invoke())
        img_field.pack(padx=10, pady=10)

        btn_save.pack(pady=40)
        cls.set_footer()

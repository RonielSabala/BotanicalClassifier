import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from common.constants import DEFAULT_IMAGE_ENTRY_TEXT
from common.utils import get_full_image_route

from ...assets.loaded_images import APP_ICON_IMAGE
from ...styles import entry_text_style, primary_button_style
from ..menu_page import MenuPage
from ..page import Page
from .utils import (
    append_record,
    get_next_image_filename,
    is_valid_image_route,
    is_valid_last_name,
    is_valid_location,
    is_valid_name,
)

# File dialog constants
FILE_DIALOG_TITLE = "Selecciona una imagen"
VALID_FILE_TYPES = [("Archivos de imagen", "*.png;*.jpg;*.jpeg")]

# - Page info:

PAGE_TITLE = "Formulario"
NAME_ENTRY_NAME = "Nombre"
LAST_NAME_ENTRY_NAME = "Apellido"
LOCATION_ENTRY_NAME = "Ubicación"
IMAGE_ENTRY_NAME = "Imagen"
SAVE_BUTTON_TEXT = "Guardar"

# Form error message
FORM_ERROR = "Se produjo un error al guardar el formulario"


def save_form() -> None:
    """
    Guarda y valida la información del formulario.
    """

    name = FormPage.name_var.get()
    last_name = FormPage.last_name_var.get()
    location = FormPage.location_var.get()
    image_route = FormPage.image_route

    # Validate entries
    if not (
        is_valid_name(name)
        and is_valid_last_name(last_name)
        and is_valid_location(location)
        and is_valid_image_route(image_route)
    ):
        return

    # Save form
    try:
        image_extension = image_route.split(".")[-1]
        image_filename = get_next_image_filename(image_extension)
        full_image_route = get_full_image_route(image_filename)

        append_record(str([name, last_name, location, full_image_route, None]))
        shutil.copy(image_route, full_image_route)
    except Exception as e:
        messagebox.showerror("Error", f"{FORM_ERROR}: {e}")
        return

    if FormPage.prev_page is None:
        return

    # Show previous page
    FormPage.prev_page.show()


class FormPage(Page):
    prev_page = MenuPage
    name_var = tk.StringVar()
    last_name_var = tk.StringVar()
    location_var = tk.StringVar()
    _image_var = tk.StringVar()
    image_route = ""

    @classmethod
    def show(cls) -> None:
        # Reset variables
        cls.name_var.set("")
        cls.last_name_var.set("")
        cls.location_var.set("")
        cls._image_var.set(DEFAULT_IMAGE_ENTRY_TEXT)
        cls.image_route = cls._image_var.get()

        super().show()

    @classmethod
    def set_entry_name(cls, entry_name: str) -> None:
        cls.set_text("", 2)
        cls.set_text(entry_name, font_size=22, fg="Black")

    @classmethod
    def load(cls) -> None:
        # Header elements
        cls.set_return_btn()
        tk.Label(cls.root, image=APP_ICON_IMAGE, bg=cls.bg_color).pack(padx=10, pady=15)
        cls.set_text(PAGE_TITLE, 35, pady=15, fg="#091518")

        # - Page elements:

        name_entry = tk.Entry(cls.root, textvariable=cls.name_var, **entry_text_style)

        last_name_entry = tk.Entry(
            cls.root, textvariable=cls.last_name_var, **entry_text_style
        )

        location_entry = tk.Entry(
            cls.root, textvariable=cls.location_var, **entry_text_style
        )

        image_entry = tk.Entry(
            cls.root,
            textvariable=cls._image_var,
            cursor="hand2",
            state="readonly",
            **entry_text_style,
        )

        save_button = tk.Button(
            cls.root,
            text=SAVE_BUTTON_TEXT,
            command=lambda: save_form(),
            **primary_button_style,
        )

        # - Elements configuration:

        cls.main_entry = name_entry

        # Name entry
        cls.set_entry_name(NAME_ENTRY_NAME)
        name_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        name_entry.bind("<Down>", lambda event: last_name_entry.focus_set())
        name_entry.bind("<Return>", lambda event: last_name_entry.focus_set())
        name_entry.pack()

        # Last name entry
        cls.set_entry_name(LAST_NAME_ENTRY_NAME)
        last_name_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        last_name_entry.bind("<Up>", lambda event: name_entry.focus_set())
        last_name_entry.bind("<Down>", lambda event: location_entry.focus_set())
        last_name_entry.bind("<Return>", lambda event: location_entry.focus_set())
        last_name_entry.pack()

        # Location entry
        cls.set_entry_name(LOCATION_ENTRY_NAME)
        location_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        location_entry.bind("<Up>", lambda event: last_name_entry.focus_set())
        location_entry.pack()

        # - Image entry:

        def on_click():
            cls.image_route = filedialog.askopenfilename(
                title=FILE_DIALOG_TITLE,
                filetypes=VALID_FILE_TYPES,
            )

            if not cls.image_route:
                return

            image_entry.config(state="normal")
            image_entry.delete(0, tk.END)
            image_entry.insert(0, cls.image_route.split("/")[-1])
            image_entry.config(state="readonly")

        cls.set_entry_name(IMAGE_ENTRY_NAME)
        image_entry.bind("<Button-1>", lambda event: on_click())
        image_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        image_entry.bind("<Up>", lambda event: location_entry.focus_set())
        image_entry.bind("<Return>", lambda event: save_button.invoke())
        image_entry.pack(padx=10, pady=10)

        # Save button
        save_button.pack(pady=40)

        cls.set_footer()

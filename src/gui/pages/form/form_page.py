import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from common.constants import VALID_IMAGE_FILE_TYPES
from common.utils import get_full_image_path
from services.i18n import i18n

from ...assets.images import APP_ICON_IMAGE
from ...page import Page
from ...styles import entry_text_style, primary_button_style
from ..menu_page import MenuPage
from .helpers import (
    append_record,
    get_next_image_filename,
    is_valid_address,
    is_valid_image_path,
    is_valid_name,
    is_valid_surname,
)


def save_form() -> None:
    """
    Guarda y valida la información del formulario.
    """

    name = FormPage.name_var.get()
    surname = FormPage.surname_var.get()
    address = FormPage.address_var.get()
    image_path = FormPage.image_path

    # Validate entries
    if not (
        is_valid_name(name)
        and is_valid_surname(surname)
        and is_valid_address(address)
        and is_valid_image_path(image_path)
    ):
        return

    # Save form
    try:
        image_extension = (image_path.split(".")[-1]).lower()
        image_filename = get_next_image_filename(image_extension)
        full_image_path = get_full_image_path(image_filename)

        append_record(str([name, surname, address, full_image_path, None]))
        shutil.copy(image_path, full_image_path)
    except Exception as e:
        save_error = i18n.get("form.save_error")
        messagebox.showerror("Error", f"{save_error}: {e}")
        return

    if FormPage.prev_page is None:
        return

    # Show previous page
    FormPage.prev_page.show()


class FormPage(Page):
    prev_page = MenuPage
    name_var = tk.StringVar()
    surname_var = tk.StringVar()
    address_var = tk.StringVar()
    _image_var = tk.StringVar()
    image_path = ""

    @classmethod
    def show(cls) -> None:
        # Reset variables
        cls.name_var.set("")
        cls.surname_var.set("")
        cls.address_var.set("")
        cls._image_var.set(i18n.get("form.utils.attach_image"))
        cls.image_path = cls._image_var.get()

        super().show()

    @classmethod
    def set_entry_name(cls, entry_name: str) -> None:
        cls.set_text("", 2)
        cls.set_text(entry_name, font_size=22, fg="Black")

    @classmethod
    def load(cls) -> None:
        # Header elements
        page_title = i18n.get("form.title")
        tk.Label(cls.root, image=APP_ICON_IMAGE, bg=cls.bg_color).pack(padx=10, pady=15)
        cls.set_text(page_title, 35, pady=15, fg="#091518")
        cls.set_return_btn()

        # - Page elements:

        name_entry = tk.Entry(cls.root, textvariable=cls.name_var, **entry_text_style)
        surname_entry = tk.Entry(
            cls.root, textvariable=cls.surname_var, **entry_text_style
        )

        address_entry = tk.Entry(
            cls.root, textvariable=cls.address_var, **entry_text_style
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
            text=i18n.get("form.save"),
            command=lambda: save_form(),
            **primary_button_style,
        )

        # - Elements configuration:

        cls.main_entry = name_entry

        # Name entry
        cls.set_entry_name(i18n.get("form.name"))
        name_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        name_entry.bind("<Down>", lambda event: surname_entry.focus_set())
        name_entry.bind("<Return>", lambda event: surname_entry.focus_set())
        name_entry.pack()

        # Surname entry
        cls.set_entry_name(i18n.get("form.surname"))
        surname_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        surname_entry.bind("<Up>", lambda event: name_entry.focus_set())
        surname_entry.bind("<Down>", lambda event: address_entry.focus_set())
        surname_entry.bind("<Return>", lambda event: address_entry.focus_set())
        surname_entry.pack()

        # Address entry
        cls.set_entry_name(i18n.get("form.address"))
        address_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        address_entry.bind("<Up>", lambda event: surname_entry.focus_set())
        address_entry.pack()

        # - Image entry:

        def on_click():
            cls.image_path = filedialog.askopenfilename(
                title=i18n.get("form.utils.attach_image"),
                filetypes=[(i18n.get("form.image_files"), VALID_IMAGE_FILE_TYPES)],
            )

            if not cls.image_path:
                return

            image_entry.config(state="normal")
            image_entry.delete(0, tk.END)
            image_entry.insert(0, cls.image_path.split("/")[-1])
            image_entry.config(state="readonly")

        cls.set_entry_name(i18n.get("form.image"))
        image_entry.bind("<Button-1>", lambda event: on_click())
        image_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        image_entry.bind("<Up>", lambda event: address_entry.focus_set())
        image_entry.bind("<Return>", lambda event: save_button.invoke())
        image_entry.pack(padx=10, pady=10)

        # Save button
        save_button.pack(pady=40)

        cls.set_footer()

"""
Form page where the user enters personal data and selects
an image.
"""

import tkinter as tk
from tkinter import filedialog

from pydantic import ValidationError

from common.constants import ALLOWED_IMAGE_EXTENSIONS_STR
from common.utils import get_clean_error_message, show_error_messagebox
from models import Record
from services import FormService, i18n

from ..assets import APP_ICON_IMAGE
from ..page import Page
from ..styles import app as app_styles, form_page as page_styles
from ..tk_enums import BindingKey


class FormPage(Page):
    name_var = tk.StringVar()
    surname_var = tk.StringVar()
    address_var = tk.StringVar()
    _image_path_var = tk.StringVar()
    image_path = ""

    # - UI Helpers:

    @classmethod
    def _add_field_label(cls, text: str) -> None:
        cls.set_empty_separator(pady=2)
        cls.set_text(text=text, **page_styles.entry_label)

    # - Event handlers:

    @classmethod
    def _on_image_select(cls, image_entry: tk.Entry) -> None:
        """
        Open a file dialog to select an image.
        """

        user_image = filedialog.askopenfilename(
            title=i18n.get("form.utils.attach_image"),
            filetypes=[(i18n.get("form.image_files"), ALLOWED_IMAGE_EXTENSIONS_STR)],
        )

        cls.image_path = user_image
        if not user_image:
            return

        image_entry.config(state="normal")
        image_entry.delete(0, tk.END)
        image_entry.insert(0, user_image.split("/")[-1])
        image_entry.config(state="readonly")

    @classmethod
    def _on_save_button(cls) -> None:
        """
        Validate form data, persist the record, and return to
        the previous page.
        """

        try:
            record = Record(
                name=cls.name_var.get(),
                surname=cls.surname_var.get(),
                address=cls.address_var.get(),
                image_path=cls.image_path,
            )
        except ValidationError as e:
            error_msg = get_clean_error_message(e)
            show_error_messagebox(error_msg)
            return

        try:
            FormService.save_form(record)
        except Exception as e:
            save_error_msg = i18n.get("form.save_error")
            show_error_messagebox(f"{save_error_msg}: {e}")
            return

        if cls.prev_page is not None:
            cls.prev_page.show()

    # - Overridden methods:

    @classmethod
    def show(cls) -> None:
        # Reset form state every time the page is shown.
        cls.name_var.set("")
        cls.surname_var.set("")
        cls.address_var.set("")
        cls._image_path_var.set(i18n.get("form.utils.attach_image"))
        cls.image_path = cls._image_path_var.get()
        super().show()

    @classmethod
    def load(cls) -> None:
        # Widgets
        name_entry = cls.get_entry()
        surname_entry = cls.get_entry()
        address_entry = cls.get_entry()
        image_entry = cls.get_entry()
        save_button = cls.get_button()

        # - Configuration:

        cls.main_entry = name_entry

        name_entry.config(textvariable=cls.name_var, **app_styles.text_entry)
        surname_entry.config(textvariable=cls.surname_var, **app_styles.text_entry)
        address_entry.config(textvariable=cls.address_var, **app_styles.text_entry)
        image_entry.config(textvariable=cls._image_path_var, **page_styles.image_entry)
        save_button.config(
            text=i18n.get("form.save"),
            command=cls._on_save_button,
            **app_styles.primary_button,
        )

        # Bindings:

        name_entry.bind(BindingKey.ESCAPE, lambda _: cls.root.focus_set())
        name_entry.bind(BindingKey.ARROW_DOWN, lambda _: surname_entry.focus_set())
        name_entry.bind(BindingKey.RETURN, lambda _: surname_entry.focus_set())

        surname_entry.bind(BindingKey.ESCAPE, lambda _: cls.root.focus_set())
        surname_entry.bind(BindingKey.ARROW_UP, lambda _: name_entry.focus_set())
        surname_entry.bind(BindingKey.ARROW_DOWN, lambda _: address_entry.focus_set())
        surname_entry.bind(BindingKey.RETURN, lambda _: address_entry.focus_set())

        address_entry.bind(BindingKey.ESCAPE, lambda _: cls.root.focus_set())
        address_entry.bind(BindingKey.ARROW_UP, lambda _: surname_entry.focus_set())
        address_entry.bind(
            BindingKey.RETURN, lambda _: cls._on_image_select(image_entry)
        )

        image_entry.bind(
            BindingKey.LEFT_CLICK, lambda _: cls._on_image_select(image_entry)
        )

        # - Layout:

        cls.set_return_button()

        # Header
        cls.get_label(image=APP_ICON_IMAGE).pack(padx=10, pady=15)
        cls.set_text(text=i18n.get("form.title"), **page_styles.title)

        # Name field
        cls._add_field_label(i18n.get("form.name"))
        name_entry.pack()

        # Surname field
        cls._add_field_label(i18n.get("form.surname"))
        surname_entry.pack()

        # Address field
        cls._add_field_label(i18n.get("form.address"))
        address_entry.pack()

        # Image field
        cls._add_field_label(i18n.get("form.image"))
        image_entry.pack(padx=10, pady=10)

        # Save button
        save_button.pack(pady=40)

        cls.set_copyright()

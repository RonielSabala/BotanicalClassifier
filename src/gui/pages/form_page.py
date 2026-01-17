import tkinter as tk
from tkinter import filedialog

from common.constants import ALLOWED_IMAGE_EXTENSIONS
from common.utils import show_error_messagebox
from models.record_model import Record
from services.form_service import FormService
from services.i18n_service import i18n

from ..assets.images import APP_ICON_IMAGE
from ..page import Page
from ..styles import app as app_styles
from ..styles import form_page as page_styles
from ..tk_enums import EventType
from .menu_page import MenuPage


class FormPage(Page):
    prev_page = MenuPage
    name_var = tk.StringVar()
    surname_var = tk.StringVar()
    address_var = tk.StringVar()
    _image_var = tk.StringVar()
    image_path = ""

    @classmethod
    def _on_image_select(cls, image_entry: tk.Entry) -> None:
        user_image = filedialog.askopenfilename(
            title=i18n.get("form.utils.attach_image"),
            filetypes=[(i18n.get("form.image_files"), ALLOWED_IMAGE_EXTENSIONS)],
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
        Guarda y valida la información del formulario.
        """

        record = Record(
            cls.name_var.get(),
            cls.surname_var.get(),
            cls.address_var.get(),
            cls.image_path,
        )

        if not FormService.validate_record(record):
            return

        try:
            FormService.save_form(record)
        except Exception as e:
            show_error_messagebox(f"{i18n.get('form.save_error')}: {e}")
            return

        # Show previous page
        prev_page = cls.prev_page
        if prev_page is not None:
            prev_page.show()

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
    def _set_entry_name(cls, entry_name: str) -> None:
        cls.set_empty_separator(pady=2)
        cls.set_text(text=entry_name, **page_styles.entry_label)

    @classmethod
    def load(cls) -> None:
        # Header elements
        cls.get_label(image=APP_ICON_IMAGE).pack(padx=10, pady=15)
        cls.set_text(text=i18n.get("form.title"), **page_styles.title)
        cls.set_return_btn()

        # Page elements
        name_entry = cls.get_entry()
        surname_entry = cls.get_entry()
        address_entry = cls.get_entry()
        image_entry = cls.get_entry()
        save_button = cls.get_button()

        # - Elements configuration:

        cls.main_entry = name_entry

        # Name entry
        cls._set_entry_name(i18n.get("form.name"))
        name_entry.config(textvariable=cls.name_var, **app_styles.text_entry)
        name_entry.bind(EventType.ESCAPE, lambda event: cls.root.focus_set())
        name_entry.bind(EventType.ARROW_DOWN, lambda event: surname_entry.focus_set())
        name_entry.bind(EventType.RETURN, lambda event: surname_entry.focus_set())
        name_entry.pack()

        # Surname entry
        cls._set_entry_name(i18n.get("form.surname"))
        surname_entry.config(textvariable=cls.surname_var, **app_styles.text_entry)
        surname_entry.bind(EventType.ESCAPE, lambda event: cls.root.focus_set())
        surname_entry.bind(EventType.ARROW_UP, lambda event: name_entry.focus_set())
        surname_entry.bind(
            EventType.ARROW_DOWN, lambda event: address_entry.focus_set()
        )
        surname_entry.bind(EventType.RETURN, lambda event: address_entry.focus_set())
        surname_entry.pack()

        # Address entry
        cls._set_entry_name(i18n.get("form.address"))
        address_entry.config(textvariable=cls.address_var, **app_styles.text_entry)
        address_entry.bind(EventType.ESCAPE, lambda event: cls.root.focus_set())
        address_entry.bind(EventType.ARROW_UP, lambda event: surname_entry.focus_set())
        address_entry.bind(
            EventType.RETURN, lambda event: cls._on_image_select(image_entry)
        )
        address_entry.pack()

        # Image entry
        cls._set_entry_name(i18n.get("form.image"))
        image_entry.config(textvariable=cls._image_var, **page_styles.image_entry)
        image_entry.bind(
            EventType.LEFT_CLICK, lambda event: cls._on_image_select(image_entry)
        )
        image_entry.pack(padx=10, pady=10)

        # Save button
        save_button.config(
            text=i18n.get("form.save"),
            command=lambda: cls._on_save_button(),
            **app_styles.primary_button,
        )
        save_button.pack(pady=40)

        cls.set_footer()

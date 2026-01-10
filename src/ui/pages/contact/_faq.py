import tkinter as tk
from tkinter import scrolledtext

from common.constants import FAQ_ROUTE

from ..page import Page
from .contact_page import Contact

PAGE_TITLE = "Preguntas Frecuentes"

# Get content
with open(FAQ_ROUTE, "r", encoding="utf-8") as f:
    faq_content = f.read()


class Faq(Page):
    prev_page = Contact

    @classmethod
    def load(cls) -> None:
        # Title
        cls.set_return_btn()
        cls.set_text("", 0, pady=35)
        cls.set_text(PAGE_TITLE, 30, pady=0, fg="#091518")
        cls.set_text("", 0, pady=25)

        # Scrollable text
        box = scrolledtext.ScrolledText(cls.root, wrap=tk.WORD, width=50, height=12)
        box.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        box.config(state=tk.NORMAL, font=("Arial", 13), relief="flat")
        box.insert(tk.END, faq_content)
        box.config(state=tk.DISABLED)
        cls.set_text("", 0, pady=35)

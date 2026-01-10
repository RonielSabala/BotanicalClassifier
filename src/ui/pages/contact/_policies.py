import tkinter as tk
from tkinter import scrolledtext

from common.constants import POLICIES_ROUTE

from ..page import Page
from .contact_page import Contact

PAGE_TITLE = "Políticas De Privacidad"

# Get content
with open(POLICIES_ROUTE, "r", encoding="utf-8") as f:
    policies_content = f.read()


class Policies(Page):
    pagina_anterior = Contact

    @classmethod
    def load(cls) -> None:
        # Title
        cls.set_return_btn()
        cls.set_text("", 0, pady=35)
        cls.set_text(PAGE_TITLE, 30, pady=0, fg="#091518")
        cls.set_text("", 0, pady=0)

        # Scrollable text
        box = scrolledtext.ScrolledText(cls.raiz, wrap=tk.WORD, width=50, height=12)
        box.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        box.config(state=tk.NORMAL, font=("Arial", 10), bg="Gray95")
        box.insert(tk.END, policies_content)
        box.config(state=tk.DISABLED)
        cls.set_text("", 0, pady=30)

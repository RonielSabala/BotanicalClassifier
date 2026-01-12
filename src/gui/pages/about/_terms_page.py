import tkinter as tk
from tkinter import scrolledtext

from common.constants import TERMS_ROUTE

from ..page import Page
from .about_page import AboutPage

# - Page info:

PAGE_TITLE = "Términos De Uso"

# Get page content
with open(TERMS_ROUTE, "r", encoding="utf-8") as f:
    page_content = f.read()


class TermsPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Header
        cls.set_return_btn()
        cls.set_text("", 0, pady=35)
        cls.set_text(PAGE_TITLE, 30, pady=0, fg="#091518")
        cls.set_text("", 0, pady=0)

        # Content
        scrollable_text = scrolledtext.ScrolledText(
            cls.root, wrap=tk.WORD, width=50, height=12
        )

        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        scrollable_text.config(state=tk.NORMAL, font=("Arial", 10), bg="Gray95")
        scrollable_text.insert(tk.END, page_content)
        scrollable_text.config(state=tk.DISABLED)
        cls.set_text("", 0, pady=30)

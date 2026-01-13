import tkinter as tk
from tkinter import scrolledtext

from common.constants import FAQ_PATH
from common.i18n import i18n

from ..page import Page
from .about_page import AboutPage

# Get page content
with open(FAQ_PATH, "r", encoding="utf-8") as f:
    page_content = f.read()


class FaqPage(Page):
    prev_page = AboutPage

    @classmethod
    def load(cls) -> None:
        # Header
        cls.set_return_btn()
        cls.set_text("", 0, pady=35)
        cls.set_text(i18n.get("about.faq.title"), 30, pady=0, fg="#091518")
        cls.set_text("", 0, pady=25)

        # Content
        scrollable_text = scrolledtext.ScrolledText(
            cls.root, wrap=tk.WORD, width=50, height=12
        )

        scrollable_text.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        scrollable_text.config(state=tk.NORMAL, font=("Arial", 13), relief="flat")
        scrollable_text.insert(tk.END, page_content)
        scrollable_text.config(state=tk.DISABLED)
        cls.set_text("", 0, pady=35)

import tkinter as tk
from tkinter import scrolledtext

from common.constants import FAQ_ROUTE

from ...main import Page
from .contact import Contact

# Get content
with open(FAQ_ROUTE, "r", encoding="utf-8") as f:
    faq_content = f.read()


class Faq(Page):
    pagina_anterior = Contact

    @classmethod
    def cargar(cls) -> None:
        # Header
        cls.colocar_retorno()
        cls.colocar_texto("", 0, pady=35)
        cls.colocar_texto("Preguntas Frecuentes", 30, pady=0, fg="#091518")
        cls.colocar_texto("", 0, pady=25)

        # Caja de texto
        box = scrolledtext.ScrolledText(cls.raiz, wrap=tk.WORD, width=50, height=12)
        box.pack(padx=85, pady=0, fill=tk.BOTH, expand=True)
        box.config(state=tk.NORMAL, font=("Arial", 13), relief="flat")
        box.insert(tk.END, faq_content)
        box.config(state=tk.DISABLED)
        cls.colocar_texto("", 0, pady=35)

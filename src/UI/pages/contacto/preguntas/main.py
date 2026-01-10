import tkinter as tk
from tkinter import scrolledtext

from ....main import Page
from ..main import Contact

info = """
P: ¿Qué es el jardín Botánico?
R: Una institución pública de carácter científico, educativo, de recreación que brinda importantes servicios ambientales.



P: ¿Cuál es la naturaleza del jardín botánico?
R: La naturaleza principal del jardín es científica y de conservación de la flora nacional.



P: ¿Cuáles son las funciones que desempeña el jardín botánico?
R: Investigación, conservación, educación ambiental y esparcimiento.



P: ¿Por qué son importantes las investigaciones científicas?
R: Porque permiten conocer la naturaleza y características de las plantas y con las informaciones producidas hacen un manejo sostenible de los   recursos florísticos y el ambiente en general.



P: ¿Qué acciones lleva a cabo el jardín botánico para conservación?
R: Estudiar el estado de conservación de la flora dominicana, colectar y conservar semillas, reproducir plantas en vivero, apoyar proyectos y programas forestales, capacitar personal en paisajismo y jardinería entre otros.



P: ¿Qué importancia tiene la educación ambiental?
R: Contribuye a crear conciencia en las personas sobre la necesidad de cuidar y manejar de forma sostenible y amigable el medio ambiente.



P: ¿Qué acciones lleva a cabo el jardín botánico para contribuir con la educación ambiental?
R: Se imparten cursos, talleres, simposios y conferencias.



P: ¿Cuáles son las instancias que componen la institución?
R: La institución cuenta con una dirección general y seis departamentos. Administración, RRHH, Botánica, Horticultura, Planificación, Educación Ambiental.



P: ¿De los servicios ofrecidos cuáles son los más solicitados?
R:
    - Identificación de plantas.
    - Labor social.
    - Asesorías de investigaciones científicas.
    - Recorrido en tren.
    - Recorrido en el herbario.
    - Entre otros.


P: ¿Cuáles son los días que el jardín botánico presta servicio al público y en que horarios?
R: De lunes a domingo en horario de 9:00 a.m. a 5:00 p.m."""


class Preguntas(Page):
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
        box.insert(tk.END, info[1:])
        box.config(state=tk.DISABLED)
        cls.colocar_texto("", 0, pady=35)

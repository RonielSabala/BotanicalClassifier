import math
import tkinter as tk
from tkinter import font, messagebox
from typing import Sequence

from ....common.constants import COLUMNA_FLOR, COLUMNA_MAX, COLUMNAS, FILA_MAX
from ....storage import main as Data
from ...assets.main import IMG_ICONO, IMG_VACIO, reescalar_imagen
from ...main import Page
from ...styles import main as Estilos
from ..formulario.main import Formulario
from ..menu.main import Menu


class Tabla(Page):
    pagina_anterior = Menu

    # Variables
    _registros: list[Sequence]
    registros: list[Sequence]
    pagina: int = 0
    max_pagina: int = 0
    flecha_derecha: tk.Button
    flecha_izquierda: tk.Button
    var_filtro = tk.StringVar()
    ultimo_filtro = (None, None)
    categoria: str = COLUMNAS[1]
    cabezales: list[tk.Button] = []

    @classmethod
    def salir(cls):
        cls.var_filtro.set("")
        cls.ultimo_filtro = None, None
        cls.main_element = None

    @classmethod
    def configurar_escenas(cls):
        Formulario.pagina_anterior = cls

    @classmethod
    def obtener_registros(cls) -> None:
        cls._registros = [()]
        for i, registro in enumerate(Data.obtener_formularios(), start=1):
            cls._registros.append([f"{i}."] + registro)

    @classmethod
    def actualizar_registros(cls) -> None:
        if cls.ultimo_filtro[0] is None:
            registros = cls._registros.copy()
        else:
            # Filtrar los registros
            filtro = cls.var_filtro.get().lower()
            columna = COLUMNAS.index(cls.categoria)
            registros = [
                x
                for x in cls._registros
                if len(x) == 0 or filtro in str(x[columna]).lower()
            ]

        # - Completar los registros:

        n = len(registros)
        if n > FILA_MAX:
            for _ in range(FILA_MAX - (n - 1) % (FILA_MAX - 1) - 1):
                registros.append([" "] * COLUMNA_MAX)

        cls.pagina = int(len(registros) != 1)
        cls.max_pagina = math.ceil((n - 1) / (FILA_MAX - 1))
        cls.registros = registros

    @classmethod
    def actualizar_tabla(cls):
        """
        Actualiza la tabla.
        """

        cls.fue_cargada = False
        cls.restablecer()
        super().mostrar()

    @classmethod
    def mostrar(cls) -> None:
        cls.configurar_escenas()
        cls.obtener_registros()
        cls.actualizar_registros()
        cls.actualizar_tabla()

    @classmethod
    def pag_anterior(cls):
        """
        Carga la pagina anterior de registros
        en la tabla.
        """

        if cls.pagina == 1:
            cls.flecha_izquierda.config(state=tk.DISABLED)
            return

        cls.pagina -= 1
        cls.actualizar_tabla()

    @classmethod
    def pag_posterior(cls):
        """
        Carga la pagina siguiente de registros
        en la tabla.
        """

        if cls.pagina == cls.max_pagina:
            cls.flecha_derecha.config(state=tk.DISABLED)
            return

        cls.pagina += 1
        cls.actualizar_tabla()

    @classmethod
    def eliminar_registros(cls):
        """
        Elimina todos los registros guardados.
        """

        if len(cls._registros) <= 1:
            return

        choice = messagebox.askyesno(
            "Confirmación",
            "¿Estas seguro de que quieres eliminar todo?\n"
            + "Esta acción no puede deshacerse.",
        )

        if not choice:
            return

        Data.limpiar_registros()
        Menu.mostrar()

    @classmethod
    def cambiar_categoria(cls, nuevo_valor: str) -> None:
        """
        Cambia la categoria a buscar.
        """

        if (ultimo_valor := cls.categoria) == nuevo_valor:
            return

        cls.categoria = nuevo_valor

        # Cambiar el estilo de los cabezales
        for cabezal in cls.cabezales:
            if (texto := cabezal["text"]) in (ultimo_valor, nuevo_valor):
                cabezal.config(
                    font=font.Font(
                        family="Arial",
                        size=16,
                        weight="bold",
                        underline=texto == nuevo_valor,
                    )
                )

    @classmethod
    def buscar_registros(cls) -> None:
        """
        Busca los registros según el texto
        introducido en el campo de texto según
        la categoria seleccionada.
        """

        temp = cls.registros.copy()
        filtro = cls.var_filtro.get(), cls.categoria
        if filtro != cls.ultimo_filtro:
            cls.ultimo_filtro = filtro
            cls.actualizar_registros()

            if temp == cls.registros:
                return

            cls.actualizar_tabla()

    @classmethod
    def clasificar_registro(cls, raiz, index: int) -> tk.Frame:
        bg = "white"
        grid = tk.Frame(raiz, bg=bg)
        grid.rowconfigure(0, weight=1)

        tk.Label(grid, text="N/A", font=("Arial", 13), bg=bg).grid(
            row=0, column=0, pady=5
        )

        def clasificar(linea: int) -> None:
            pagina = cls.pagina
            Data.insertar_clasificacion(linea)
            cls.obtener_registros()
            cls.actualizar_registros()
            cls.pagina = pagina
            cls.actualizar_tabla()

        btn = tk.Button(
            grid,
            text="Clasificar",
            command=lambda valor=index: clasificar(valor),
            **Estilos.btn_primario,
        )
        btn.config(
            font=("Arial", 16, "bold"),
            fg="Black",
            bg=bg,
            activebackground=bg,
            activeforeground="VioletRed3",
        )
        btn.grid(row=2, column=0)

        return grid

    @classmethod
    def tabla_prediccion(cls, raiz, data) -> tk.Frame:
        grid = tk.Frame(raiz)

        # Cabezales
        for i, texto in enumerate(("Tag", "Probabilidad")):
            tk.Label(
                grid,
                text=texto,
                font=("Arial", 12 if i == 0 else 10, "bold"),
                fg="White" if i == 0 else "GoldenRod1",
                bg="Gray15",
            ).grid(row=0, column=i, sticky="nsew", padx=0)

        # Contenido
        for i, prediccion in enumerate(
            sorted(data, key=lambda item: item[1], reverse=True)
        ):
            for j, dato in enumerate(prediccion):
                if j == 0:
                    dato = dato.capitalize()
                else:
                    dato = f"{dato:.2%} " + ("✔" if i == 0 else "✗")

                tk.Label(
                    grid,
                    text=dato,
                    font=("Arial", 10),
                    fg="Black" if i == 0 else f"Gray{60 + 8 * i}",
                    bg="GoldenRod1" if i == 0 else "White",
                ).grid(row=i + 1, column=j, sticky="nsew")

        return grid

    @classmethod
    def cargar(cls) -> None:
        # - Header:

        cls.colocar_retorno()
        tk.Label(cls.raiz, image=IMG_ICONO, bg=cls.color_fondo).pack(padx=20, pady=15)
        cls.colocar_texto("Registros", 32, pady=0, fg="#091518")
        cls.colocar_texto("", 0, pady=2)

        # - Grid de registros:

        grid = cls.obtener_grid()
        grid.pack(fill="both", padx=20, pady=0)

        # Buscador de registros
        buscador = tk.Entry(grid, textvariable=cls.var_filtro, **Estilos.campo_txt)
        buscador.config(width=30)
        buscador.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=10)
        buscador.bind("<Escape>", lambda event: cls.raiz.focus_set())
        buscador.bind("<Return>", lambda event: btn_buscar.invoke())
        if cls.ultimo_filtro[0] is not None:
            cls.main_element = buscador

        # Botón de buscar
        btn_buscar = tk.Button(
            grid,
            text="Buscar",
            font=("Arial", 13),
            command=lambda: cls.buscar_registros(),
            cursor="hand2",
        )

        btn_buscar.grid(row=0, column=4, sticky="w")

        # - Insertar registros en el grid:

        cls.cabezales = []
        index = (FILA_MAX - 1) * (cls.pagina - 1)
        for fila, data in enumerate(cls.registros[index : index + FILA_MAX + 1]):
            if fila == 0:
                data = COLUMNAS

            elif fila == FILA_MAX:
                break

            # Insertar fila
            for columna, sub_data in enumerate(data):
                # Color de las filas
                fg, bg = "Black", cls.color_fondo
                if columna > 0:
                    if fila == 0:
                        # Cabezales
                        fg, bg = "white", "Dodgerblue4"
                    elif columna != COLUMNA_MAX - 1 and sub_data != " ":
                        # Registros
                        bg = "Gray96" if fila % 2 else "Gray92"

                # Crear una imagen
                if fila > 0 and columna == COLUMNA_FLOR:
                    img = (
                        reescalar_imagen(sub_data)
                        if Data.es_ruta(sub_data)
                        else IMG_VACIO
                    )

                    elemento = tk.Label(grid, image=img)
                    elemento.image = img  # type: ignore

                # Crear un label o botón
                else:
                    fuente = "Arial", 16, "bold"

                    # Botón de predecir
                    if sub_data is None:
                        elemento = cls.clasificar_registro(
                            grid, int(cls.registros[index + fila][0][:-1])
                        )

                        elemento.grid(row=fila + 1, column=columna, padx=0, pady=1)

                        continue

                    # Predicciones
                    elif sub_data != " " and fila > 0 and columna == COLUMNA_MAX - 1:
                        elemento = cls.tabla_prediccion(grid, sub_data)
                        elemento.config(bg=bg)
                        elemento.grid(row=fila + 1, column=columna)
                        continue

                    # Crear un label
                    elif fila > 0 or columna in (0, COLUMNA_FLOR, COLUMNA_MAX - 1):
                        elemento = tk.Label(grid)
                        if fila > 0:
                            fuente = "Segoe UI Emoji", 13
                            if columna > 0:
                                elemento.config(cursor="xterm")

                    # Crear un botón
                    else:
                        if cls.categoria == sub_data:
                            fuente += ("underline",)

                        elemento = tk.Button(
                            grid,
                            border=0,
                            activeforeground="Black",
                            activebackground="DodgerBlue4",
                            cursor="hand2",
                            command=lambda valor=sub_data: cls.cambiar_categoria(valor),
                        )

                        cls.cabezales.append(elemento)

                    elemento.config(
                        text=sub_data,
                        font=fuente,
                        relief="flat",
                    )

                    # Anchor
                    if columna in (0, 1):
                        elemento.config(
                            anchor=(
                                "center"
                                if fila in (0, FILA_MAX)
                                else ("e" if columna == 0 else "w")
                            ),
                            padx=15,
                        )

                elemento.config(fg=fg, bg=bg)
                elemento.grid(
                    row=fila + 1,
                    column=columna,
                    sticky="nsew",
                    pady=1,
                )

        # - Grid de navegación:

        grid_nav = cls.obtener_grid()
        grid_nav.pack(fill="none", padx=35, pady=0)

        # Flecha para retroceder
        cls.flecha_izquierda = tk.Button(
            grid_nav,
            text="<",
            command=cls.pag_anterior,
            font=("Arial", 24),
            **Estilos.flecha_nav,
        )
        cls.flecha_izquierda.grid(row=0, column=0, sticky="nsew", padx=0, pady=5)

        # Número de páginas
        tk.Label(
            grid_nav,
            text=f"pagina {cls.pagina} de {cls.max_pagina}",
            fg="Black",
            bg=cls.color_fondo,
            font=("Arial", 14),
        ).grid(row=0, column=1, sticky="nsew", padx=0, pady=5)

        # Flecha para avanzar
        cls.flecha_derecha = tk.Button(
            grid_nav,
            text=">",
            command=cls.pag_posterior,
            font=("Arial", 24),
            **Estilos.flecha_nav,
        )
        cls.flecha_derecha.grid(row=0, column=2, sticky="nsew", padx=0, pady=5)

        # - Configuración:

        if cls.pagina <= 1:
            cls.flecha_izquierda.config(state=tk.DISABLED)
        else:
            cls.flecha_izquierda.config(cursor="hand2")

        if cls.pagina >= cls.max_pagina:
            cls.flecha_derecha.config(state=tk.DISABLED)
        else:
            cls.flecha_derecha.config(cursor="hand2")

        cls.colocar_texto("", 0, pady=2)

        # Botón para añadir registros
        btn_añadir = tk.Button(
            cls.raiz,
            text="✚ Añadir",
            command=Formulario.mostrar,
            **Estilos.btn_añadir,  # type: ignore
        )
        btn_añadir.pack(pady=0)

        # Botón para eliminar todos los registros
        btn_eliminar = tk.Button(
            cls.raiz,
            text="✘ Eliminar (TODO)",
            command=cls.eliminar_registros,
            **Estilos.btn_eliminar,  # type: ignore
        )
        btn_eliminar.pack(pady=12)

        # - Footer:

        cls.colocar_footer()

import tkinter as tk
from tkinter import Frame, font, messagebox
from typing import Optional, Sequence

from common.utils import is_valid_route
from ui.assets.loaded_images import EMPTY_IMAGE, get_resized_image

from ...assets.loaded_images import APP_ICON_IMAGE
from ...styles import (
    add_button_style,
    delete_button_style,
    entry_text_style,
    navigation_arrow_style,
    primary_button_style,
)
from ..form.form_page import FormPage
from ..menu_page import MenuPage
from ..page import Page
from .utils import clean_records, get_records, insert_record_prediction

# - Table constants:

_RECORD_NUMERATION_COLUMN_NAME = " "
_OWNER_COLUMN_NAME = "Subido por"
_LAST_NAME_COLUMN_NAME = "Apellido"
_LOCATION_COLUMN_NAME = "Ubicación"
_FLOWER_COLUMN_NAME = "Flor"
_PREDICTION_COLUMN_NAME = "Predicción"
COLUMN_NAMES = (
    _RECORD_NUMERATION_COLUMN_NAME,
    _OWNER_COLUMN_NAME,
    _LAST_NAME_COLUMN_NAME,
    _LOCATION_COLUMN_NAME,
    _FLOWER_COLUMN_NAME,
    _PREDICTION_COLUMN_NAME,
)


MAX_ROW_INDEX_PER_PAGE = 3
MAX_COLUMN_INDEX = len(COLUMN_NAMES) - 1
FLOWER_COLUMN_INDEX = COLUMN_NAMES.index(_FLOWER_COLUMN_NAME)

# - GUI constants:

PAGE_TITLE = "Registros"
SEARCH_BUTTON_TEXT = "Buscar"

PAGE_NUMBER_LABEL = "página"
PAGE_NUMBER_SEPARATOR = "de"
LEFT_NAV_ARROW_BUTTON_TEXT = ">"
RIGHT_NAV_ARROW_BUTTON_TEXT = "<"

_ADD_RECORD_BUTTON_EMOJI = "✚"
_ADD_RECORD_BUTTON_TEXT = "Añadir"
ADD_RECORD_BUTTON_TEXT = f"{_ADD_RECORD_BUTTON_EMOJI} {_ADD_RECORD_BUTTON_TEXT}"

_DELETE_ALL_RECORDS_BUTTON_EMOJI = "✘"
_DELETE_ALL_RECORDS_BUTTON_TEXT = "Eliminar (TODO)"
DELETE_ALL_RECORDS_BUTTON_TEXT = (
    f"{_DELETE_ALL_RECORDS_BUTTON_EMOJI} {_DELETE_ALL_RECORDS_BUTTON_TEXT}"
)

DELETE_ALL_DIALOG_TITLE = "Confirmación"
DELETE_ALL_DIALOG_TEXT = (
    "¿Estas seguro de que quieres eliminar todo?\nEsta acción no puede deshacerse."
)

CLASSIFY_BUTTON_TEXT = "Clasificar"
DEFAULT_CLASSIFIED_RECORD_VALUE = "N/A"
PREDICTION_TAG_COLUMN_NAME = "Tag"
PREDICTION_PROBABILITY_COLUMN_NAME = "Probabilidad"
HIGHEST_FLOWER_PROBABILITY_EMOJI = "✔"
FAILED_FLOWER_PROBABILITY_EMOJI = "✗"


class Records(Page):
    prev_page = MenuPage

    column_buttons: list[tk.Button] = []

    records: list[Sequence]
    _records: list[Sequence]

    page_index: int = 0
    max_page_index: int = 0

    left_nav_arrow: tk.Button
    right_nav_arrow: tk.Button

    filter_var = tk.StringVar()
    last_filter: tuple[Optional[str], Optional[str]] = (None, None)
    filter_column: str = _OWNER_COLUMN_NAME

    @classmethod
    def config_pages(cls):
        FormPage.prev_page = cls

    @classmethod
    def close(cls) -> None:
        cls.main_entry = None
        cls.last_filter = None, None
        cls.filter_var.set("")

    @classmethod
    def _update_table(cls):
        """
        Actualiza la tabla.
        """

        cls.is_loaded = False
        cls.reset()
        super().show()

    @classmethod
    def _fill_records(cls) -> None:
        cls._records = [()]
        for i, record in enumerate(get_records(), start=1):
            record = [f"{i}."] + record
            cls._records.append(record)

    @classmethod
    def _update_records(cls) -> None:
        # Get records
        if cls.last_filter[0] is None:
            filtered_records = cls._records.copy()
        else:
            text_to_filter = cls.filter_var.get().lower()
            filter_column_index = COLUMN_NAMES.index(cls.filter_column)
            filtered_records = [
                record
                for record in cls._records
                if len(record) == 0
                or text_to_filter in str(record[filter_column_index]).lower()
            ]

        max_record_index = len(filtered_records) - 1
        last_page_index, last_page_records_count = divmod(
            max_record_index, MAX_ROW_INDEX_PER_PAGE
        )

        # Add empty records to fill the table
        if max_record_index >= MAX_ROW_INDEX_PER_PAGE + 1:
            for _ in range(MAX_ROW_INDEX_PER_PAGE - last_page_records_count):
                filtered_records.append([" "] * (MAX_COLUMN_INDEX + 1))

        cls.records = filtered_records
        cls.page_index = int(len(filtered_records) != 1)
        cls.max_page_index = last_page_index + 1

    @classmethod
    def show(cls) -> None:
        cls.config_pages()
        cls._fill_records()
        cls._update_records()
        cls._update_table()

    @classmethod
    def _load_prev_page(cls):
        """
        Carga la pagina anterior de registros
        en la tabla.
        """

        if cls.page_index == 1:
            cls.right_nav_arrow.config(state=tk.DISABLED)
            return

        cls.page_index -= 1
        cls._update_table()

    @classmethod
    def _load_next_page(cls):
        """
        Carga la pagina siguiente de registros
        en la tabla.
        """

        if cls.page_index == cls.max_page_index:
            cls.left_nav_arrow.config(state=tk.DISABLED)
            return

        cls.page_index += 1
        cls._update_table()

    @classmethod
    def _delete_all_records(cls):
        """
        Elimina todos los registros guardados.
        """

        if len(cls._records) == 0:
            return

        choice = messagebox.askyesno(DELETE_ALL_DIALOG_TITLE, DELETE_ALL_DIALOG_TEXT)
        if not choice:
            return

        clean_records()
        MenuPage.show()

    @classmethod
    def _update_filter_column(cls, filter_column: str) -> None:
        """
        Cambia la categoría a buscar.
        """

        prev_filter_column = cls.filter_column
        if filter_column == prev_filter_column:
            return

        cls.filter_column = filter_column

        # Update column buttons
        for col_button in cls.column_buttons:
            button_text = col_button["text"]
            if button_text not in (prev_filter_column, filter_column):
                continue

            col_button.config(
                font=font.Font(
                    family="Arial",
                    size=16,
                    weight="bold",
                    underline=button_text == filter_column,
                )
            )

    @classmethod
    def _filter_records(cls) -> None:
        """
        Busca los registros según el texto
        introducido en el campo de texto según
        la categoría seleccionada.
        """

        current_filter = cls.filter_var.get(), cls.filter_column
        if current_filter == cls.last_filter:
            return

        prev_records = cls.records.copy()
        cls.last_filter = current_filter
        cls._update_records()
        if cls.records == prev_records:
            return

        cls._update_table()

    @classmethod
    def _classify_record(cls, record_index: int) -> None:
        prev_page_index = cls.page_index

        insert_record_prediction(record_index)
        cls._fill_records()
        cls._update_records()

        cls.page_index = prev_page_index
        cls._update_table()

    @classmethod
    def _get_classified_record_grid(cls, root: Frame, record_index: int) -> Frame:
        bg_color = "white"
        grid = Frame(root, bg=bg_color)
        grid.rowconfigure(0, weight=1)
        tk.Label(
            grid,
            text=DEFAULT_CLASSIFIED_RECORD_VALUE,
            font=("Arial", 13),
            bg=bg_color,
        ).grid(row=0, column=0, pady=5)

        # Create classification button
        button = tk.Button(
            grid,
            text=CLASSIFY_BUTTON_TEXT,
            command=lambda record_index=record_index: cls._classify_record(
                record_index
            ),
            **primary_button_style,
        )

        # Button config
        button.config(
            font=("Arial", 16, "bold"),
            fg="Black",
            bg=bg_color,
            activebackground=bg_color,
            activeforeground="VioletRed3",
        )

        button.grid(row=2, column=0)
        return grid

    @classmethod
    def _get_prediction_grid(
        cls, root: Frame, predictions: list[tuple[str, float]]
    ) -> Frame:
        grid = Frame(root)
        prediction_column_names = (
            PREDICTION_TAG_COLUMN_NAME,
            PREDICTION_PROBABILITY_COLUMN_NAME,
        )

        # Add column names
        for i, column_name in enumerate(prediction_column_names):
            tk.Label(
                grid,
                text=column_name,
                font=("Arial", 12 if i == 0 else 10, "bold"),
                fg="White" if i == 0 else "GoldenRod1",
                bg="Gray15",
            ).grid(row=0, column=i, sticky="nsew", padx=0)

        sorted_predictions = sorted(
            predictions, key=lambda probability: probability[1], reverse=True
        )

        # Add predictions
        for i, prediction in enumerate(sorted_predictions):
            for j, data in enumerate(prediction):
                if isinstance(data, str):
                    data = data.capitalize()
                else:
                    data = f"{data:.2%} " + (
                        HIGHEST_FLOWER_PROBABILITY_EMOJI
                        if i == 0
                        else FAILED_FLOWER_PROBABILITY_EMOJI
                    )

                tk.Label(
                    grid,
                    text=data,
                    font=("Arial", 10),
                    fg="Black" if i == 0 else f"Gray{60 + 8 * i}",
                    bg="GoldenRod1" if i == 0 else "White",
                ).grid(row=i + 1, column=j, sticky="nsew")

        return grid

    @classmethod
    def _fill_records_grid(cls, records_grid: Frame) -> None:
        cls.column_buttons = []
        start_index = MAX_ROW_INDEX_PER_PAGE * (cls.page_index - 1)

        row_data = None
        for row in range(start_index, start_index + MAX_ROW_INDEX_PER_PAGE + 1):
            if row_data is None:
                row_data = COLUMN_NAMES
            else:
                row_data = cls.records[row]

            # Insert row
            for col, cell_data in enumerate(row_data):
                # Row color
                fg_color, bg_color = "Black", cls.bg_color
                if col > 0:
                    # Column names
                    if row == 0:
                        fg_color, bg_color = "white", "Dodgerblue4"

                    # Records
                    elif col != MAX_COLUMN_INDEX and cell_data != " ":
                        bg_color = "Gray96" if row % 2 else "Gray92"

                # Insert the flower image
                if row > 0 and col == FLOWER_COLUMN_INDEX:
                    image = (
                        get_resized_image(cell_data)
                        if is_valid_route(cell_data)
                        else EMPTY_IMAGE
                    )

                    # Configure image
                    item = tk.Label(records_grid, image=image)

                # Insert a label/button
                else:
                    font = "Arial", 16, "bold"

                    # Insert predict button
                    if cell_data is None:
                        record_index = int(cls.records[start_index + row][0][:-1]) - 1
                        item = cls._get_classified_record_grid(
                            records_grid, record_index
                        )
                        item.grid(row=row + 1, column=col, padx=0, pady=1)
                        continue

                    # Insert predictions grid
                    elif cell_data != " " and row > 0 and col == MAX_COLUMN_INDEX:
                        item = cls._get_prediction_grid(records_grid, cell_data)  # type: ignore
                        item.config(bg=bg_color)
                        item.grid(row=row + 1, column=col)
                        continue

                    # Insert label
                    elif row > 0 or col in (
                        0,
                        FLOWER_COLUMN_INDEX,
                        MAX_COLUMN_INDEX,
                    ):
                        item = tk.Label(records_grid)
                        if row > 0:
                            font = "Segoe UI Emoji", 13
                            if col > 0:
                                item.config(cursor="xterm")

                    # Insert button
                    else:
                        if cls.filter_column == cell_data:
                            font += ("underline",)

                        item = tk.Button(
                            records_grid,
                            border=0,
                            activeforeground="Black",
                            activebackground="DodgerBlue4",
                            cursor="hand2",
                            command=lambda valor=cell_data: cls._update_filter_column(
                                valor
                            ),
                        )

                        cls.column_buttons.append(item)

                    item.config(
                        text=cell_data,
                        font=font,
                        relief="flat",
                    )

                    # Configure item anchor
                    if col in (0, 1):
                        item.config(
                            anchor=(
                                "center"
                                if row in (0, MAX_ROW_INDEX_PER_PAGE + 1)
                                else ("e" if col == 0 else "w")
                            ),
                            padx=15,
                        )

                # Configure item
                item.config(fg=fg_color, bg=bg_color)
                item.grid(row=row + 1, column=col, sticky="nsew", pady=1)

    @classmethod
    def load(cls) -> None:
        # Header elements
        cls.set_return_btn()
        tk.Label(cls.root, image=APP_ICON_IMAGE, bg=cls.bg_color).pack(padx=20, pady=15)
        cls.set_text(PAGE_TITLE, 32, pady=0, fg="#091518")
        cls.set_text("", 0, pady=2)

        # - Page elements:

        records_grid = cls.get_grid_from_root()
        navigation_grid = cls.get_grid_from_root()

        search_entry = tk.Entry(
            records_grid, textvariable=cls.filter_var, **entry_text_style
        )

        search_button = tk.Button(
            records_grid,
            text=SEARCH_BUTTON_TEXT,
            font=("Arial", 13),
            command=lambda: cls._filter_records(),
            cursor="hand2",
        )

        cls.left_nav_arrow = tk.Button(
            navigation_grid,
            text=LEFT_NAV_ARROW_BUTTON_TEXT,
            command=cls._load_next_page,
            font=("Arial", 24),
            **navigation_arrow_style,
        )

        cls.right_nav_arrow = tk.Button(
            navigation_grid,
            text=RIGHT_NAV_ARROW_BUTTON_TEXT,
            command=cls._load_prev_page,
            font=("Arial", 24),
            **navigation_arrow_style,
        )

        page_number_label = tk.Label(
            navigation_grid,
            text=f"{PAGE_NUMBER_LABEL} {cls.page_index} {PAGE_NUMBER_SEPARATOR} {cls.max_page_index}",
            fg="Black",
            bg=cls.bg_color,
            font=("Arial", 14),
        )

        add_record_button = tk.Button(
            cls.root,
            text=ADD_RECORD_BUTTON_TEXT,
            command=FormPage.show,
            **add_button_style,  # type: ignore
        )

        delete_all_records_button = tk.Button(
            cls.root,
            text=DELETE_ALL_RECORDS_BUTTON_TEXT,
            command=cls._delete_all_records,
            **delete_button_style,  # type: ignore
        )

        # - Elements configuration:

        if cls.last_filter[0] is not None:
            cls.main_entry = search_entry

        records_grid.pack(fill="both", padx=20, pady=0)
        navigation_grid.pack(fill="none", padx=35, pady=0)

        search_entry.config(width=30)
        search_entry.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=10)
        search_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        search_entry.bind("<Return>", lambda event: search_button.invoke())

        search_button.grid(row=0, column=4, sticky="w")

        page_number_label.grid(row=0, column=1, sticky="nsew", padx=0, pady=5)
        cls.left_nav_arrow.grid(row=0, column=2, sticky="nsew", padx=0, pady=5)
        cls.right_nav_arrow.grid(row=0, column=0, sticky="nsew", padx=0, pady=5)

        # Left arrow state config
        if cls.page_index >= cls.max_page_index:
            cls.left_nav_arrow.config(state=tk.DISABLED)
        else:
            cls.left_nav_arrow.config(cursor="hand2")

        # Right arrow state config
        if cls.page_index <= 1:
            cls.right_nav_arrow.config(state=tk.DISABLED)
        else:
            cls.right_nav_arrow.config(cursor="hand2")

        cls.set_text("", 0, pady=1)
        add_record_button.pack(pady=0)
        delete_all_records_button.pack(pady=12)

        cls.set_footer()
        cls._fill_records_grid(records_grid)

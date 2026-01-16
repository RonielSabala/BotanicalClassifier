import tkinter as tk
from tkinter import Frame, messagebox
from typing import Any, Optional

from common.utils import is_valid_path
from gui.assets.images import EMPTY_IMAGE, get_resized_image
from models.prediction_model import Prediction
from models.record_model import Record
from models.search_filter_model import SearchFilter
from services.i18n_service import i18n
from services.records_service import RecordsService

from ..assets.images import APP_ICON_IMAGE
from ..page import Page
from ..styles import app as app_styles
from ..styles import records_page as page_styles
from ..tk_events import EventType
from .form_page import FormPage
from .menu_page import MenuPage

# Table defaults
MAX_ROW_INDEX_PER_PAGE = 3

# GUI defaults
LEFT_NAV_ARROW_BUTTON_TEXT = ">"
RIGHT_NAV_ARROW_BUTTON_TEXT = "<"
ADD_RECORD_BUTTON_EMOJI = "✚"
DELETE_RECORDS_BUTTON_EMOJI = "✘"
HIGHEST_FLOWER_PROBABILITY_EMOJI = "✔"
FAILED_FLOWER_PROBABILITY_EMOJI = "✗"


class RecordsPage(Page):
    prev_page = MenuPage

    # Records variables
    _all_records: list[Record]
    _filtered_records: list[Optional[Record]]
    _filter_var: tk.StringVar = tk.StringVar()
    _last_filter: SearchFilter = SearchFilter()

    # Columns variables
    _column_names: tuple[str, ...]
    _column_buttons: list[tk.Button] = []
    _filter_column_name: str = i18n.get("records.owner_column")
    _max_column_index: int = 5
    _flower_column_index: int = 4

    # Navigation variables
    _page_index: int = 0
    _max_page_index: int = 0
    _left_nav_arrow: tk.Button
    _right_nav_arrow: tk.Button

    @classmethod
    def close(cls) -> None:
        cls.main_entry = None
        cls._last_filter.reset()
        cls._filter_var.set("")

    @classmethod
    def config_pages(cls) -> None:
        FormPage.prev_page = cls

    @classmethod
    def _update_column_names(cls) -> None:
        cls._column_names = (
            "",  # Record index column
            i18n.get("records.owner_column"),
            i18n.get("records.surname_column"),
            i18n.get("records.address_column"),
            i18n.get("records.flower_column"),
            i18n.get("records.prediction_column"),
        )

    @classmethod
    def _fill_records(cls) -> None:
        cls._all_records = list(RecordsService.load_all_records())

    @classmethod
    def _filter_records(cls) -> None:
        if cls._last_filter.search_text is None:
            cls._filtered_records = cls._all_records.copy()  # type: ignore
            return

        text_to_filter = cls._filter_var.get().lower()
        filter_column_index = cls._column_names.index(cls._filter_column_name) - 1
        cls._filtered_records = []
        for record in cls._all_records:
            record_property = RecordsService.get_record_property_by_index(
                record, filter_column_index
            )

            if text_to_filter not in record_property.lower():
                continue

            cls._filtered_records.append(record)

    @classmethod
    def _update_records(cls) -> None:
        cls._filter_records()
        max_record_index = len(cls._filtered_records) - 1
        if max_record_index == -1:
            cls._page_index = 0
            cls._max_page_index = 0
            return

        last_page_index, last_page_records_count = divmod(
            max_record_index, MAX_ROW_INDEX_PER_PAGE
        )

        cls._page_index = 1
        cls._max_page_index = last_page_index + 1
        if max_record_index < MAX_ROW_INDEX_PER_PAGE:
            return

        missing_records = [None] * (MAX_ROW_INDEX_PER_PAGE - last_page_records_count)
        cls._filtered_records.extend(missing_records)

    @classmethod
    def _update_table(cls) -> None:
        """
        Actualiza la tabla.
        """

        cls.is_loaded = False
        cls.reset()
        super().show()

    @classmethod
    def show(cls) -> None:
        cls.config_pages()
        cls._update_column_names()
        cls._fill_records()
        cls._update_records()
        cls._update_table()

    @classmethod
    def _load_prev_page(cls) -> None:
        """
        Carga la pagina anterior de registros
        en la tabla.
        """

        if cls._page_index == 1:
            cls._right_nav_arrow.config(state=tk.DISABLED)
            return

        cls._page_index -= 1
        cls._update_table()

    @classmethod
    def _load_next_page(cls) -> None:
        """
        Carga la pagina siguiente de registros
        en la tabla.
        """

        if cls._page_index == cls._max_page_index:
            cls._left_nav_arrow.config(state=tk.DISABLED)
            return

        cls._page_index += 1
        cls._update_table()

    @classmethod
    def _on_delete_click(cls) -> None:
        """
        Elimina todos los registros guardados.
        """

        if not cls._all_records:
            return

        choice = messagebox.askyesno(
            i18n.get("records.delete_dialog_title"),
            i18n.get("records.delete_dialog_text"),
        )

        if not choice:
            return

        RecordsService.delete_all_records()
        MenuPage.show()

    @classmethod
    def _on_column_name_click(cls, filter_column: str) -> None:
        """
        Cambia la categoría a buscar.
        """

        prev_filter_column = cls._filter_column_name
        if filter_column == prev_filter_column:
            return

        cls._filter_column_name = filter_column

        # Update buttons font
        for col_button in cls._column_buttons:
            button_text = col_button["text"]
            if button_text == filter_column:
                col_button.config(font=page_styles.column_filter_font)
            elif button_text == prev_filter_column:
                col_button.config(font=page_styles.column_font)

    @classmethod
    def _on_filter(cls) -> None:
        """
        Busca los registros según el texto
        introducido en el campo de texto según
        la categoría seleccionada.
        """

        current_filter = SearchFilter(cls._filter_var.get(), cls._filter_column_name)
        if current_filter == cls._last_filter:
            return

        prev_records = cls._filtered_records.copy()
        cls._last_filter = current_filter
        cls._update_records()
        if cls._filtered_records == prev_records:
            return

        cls._update_table()

    @classmethod
    def _classify_record(cls, record_id: int) -> None:
        prev_page_index = cls._page_index

        RecordsService.set_record_prediction(record_id)
        cls._fill_records()
        cls._update_records()

        cls._page_index = prev_page_index
        cls._update_table()

    @classmethod
    def _get_classification_button(cls, root: Frame, record_id: int) -> Frame:
        grid = cls.get_grid(root)
        grid.rowconfigure(0, weight=1)

        # Insert label
        label = cls.get_label(grid)
        label.config(**page_styles.classification_label)
        label.grid(row=0, column=0, pady=5)

        button_style = page_styles.classify_button.copy()
        button_style.pop("bg")
        button_style.pop("activebackground")

        # Insert button
        button = cls.get_button(grid)
        button.config(
            text=i18n.get("records.classify_button"),
            command=lambda record_id=record_id: cls._classify_record(record_id),
            **button_style,
        )
        button.grid(row=2, column=0)

        return grid

    @classmethod
    def _insert_prediction_cell(
        cls, root: Frame, row: int, col: int, cell_value: str
    ) -> None:
        cell_style = (
            page_styles.top_prediction_cell if row == 1 else page_styles.prediction_cell
        )

        tk.Label(root, text=cell_value, **cell_style).grid(
            row=row, column=col, sticky="nsew"
        )

    @classmethod
    def _get_prediction_grid(cls, root: Frame, predictions: list[Prediction]) -> Frame:
        grid = cls.get_grid(root)

        # Insert tag cell
        tk.Label(
            grid,
            text=i18n.get("records.prediction_tag_column"),
            **page_styles.tag_column_cell,
        ).grid(row=0, column=0, padx=0, sticky="nsew")

        # Insert probability cell
        tk.Label(
            grid,
            text=i18n.get("records.prediction_probability_column"),
            **page_styles.probability_column_cell,
        ).grid(row=0, column=1, padx=0, sticky="nsew")

        # Insert predictions
        for row, prediction in enumerate(predictions):
            tag_name = prediction.tag_name.capitalize()
            probability = f"{prediction.probability:.2%} " + (
                HIGHEST_FLOWER_PROBABILITY_EMOJI
                if row == 0
                else FAILED_FLOWER_PROBABILITY_EMOJI
            )

            cls._insert_prediction_cell(grid, row + 1, 0, tag_name)
            cls._insert_prediction_cell(grid, row + 1, 1, probability)

        return grid

    @classmethod
    def _get_cell_style(cls, row: int, col: int) -> dict[str, Any]:
        if col == 0:
            return page_styles.cell
        if row == 0:
            return page_styles.column_cell
        if row % 2:
            return page_styles.odd_row_cell

        return page_styles.even_row_cell

    @classmethod
    def _get_cell_element(
        cls, root: Frame, row: int, col: int, cell_value: str
    ) -> tk.Label | tk.Button:
        # Flower image
        if row > 0 and col == cls._flower_column_index:
            cell_image = (
                get_resized_image(cell_value)
                if is_valid_path(cell_value)
                else EMPTY_IMAGE
            )

            return cls.get_label(root, image=cell_image)

        # Label
        element_font = page_styles.column_font
        if row > 0 or col in (0, cls._flower_column_index, cls._max_column_index):
            element = tk.Label(root)
            if row > 0:
                element_font = page_styles.cell_font
                if col > 0:
                    element.config(cursor="xterm")

        # Button
        else:
            # Underline filter column
            if cell_value == cls._filter_column_name:
                element_font = page_styles.column_filter_font

            element = cls.get_button(root)
            element.config(
                command=lambda value=cell_value: cls._on_column_name_click(value),
                **page_styles.column_button,
            )

            cls._column_buttons.append(element)

        element.config(text=cell_value, relief="flat", font=element_font)
        if col not in (0, 1):
            return element

        # Configure item anchor
        element_anchor = "center" if row == 0 else ("e" if col == 0 else "w")
        element.config(anchor=element_anchor, padx=15)
        return element

    @classmethod
    def _fill_records_grid(cls, grid: Frame) -> None:
        cls._column_buttons = []
        first_record_index = max(0, MAX_ROW_INDEX_PER_PAGE * (cls._page_index - 1))
        last_record_index = min(
            first_record_index + MAX_ROW_INDEX_PER_PAGE, len(cls._filtered_records) - 1
        )

        record_indices = range(first_record_index - 1, last_record_index + 1)
        for row, record_index in enumerate(record_indices):
            if row == MAX_ROW_INDEX_PER_PAGE + 1:
                break

            # Get row cells
            insert_empty_row = False
            if row == 0:
                row_cells = cls._column_names
            else:
                record = cls._filtered_records[record_index]
                record_id = record.record_id if isinstance(record, Record) else -1
                if record is None:
                    insert_empty_row = True
                    row_cells = tuple(None for _ in range(cls._max_column_index + 1))
                else:
                    row_cells = (
                        f"{record_id + 1}.",
                        record.name,
                        record.surname,
                        record.address,
                        record.image_path,
                        record.predictions,
                    )

            # Insert row
            for col, cell_value in enumerate(row_cells):
                # Insert empty cell
                if insert_empty_row:
                    if col == cls._flower_column_index:
                        cell_element = cls.get_label(grid, EMPTY_IMAGE)
                    else:
                        cell_element = cls.get_label(grid)

                # Insert classification button
                elif cell_value is None:
                    button = cls._get_classification_button(grid, record_id)
                    button.grid(row=row + 1, column=col, padx=0, pady=1)
                    continue

                # Insert predictions grid
                elif isinstance(cell_value, list):
                    sorted_predictions = sorted(
                        cell_value,
                        key=lambda prediction: prediction.probability,
                        reverse=True,
                    )

                    cls._get_prediction_grid(grid, sorted_predictions).grid(
                        row=row + 1, column=col
                    )

                    continue

                # Insert button/label
                else:
                    cell_styles = {"bg": cls.bg_color, **cls._get_cell_style(row, col)}
                    cell_element = cls._get_cell_element(grid, row, col, cell_value)
                    cell_element.config(**cell_styles)

                cell_element.grid(row=row + 1, column=col, pady=1, sticky="nsew")

    @classmethod
    def load(cls) -> None:
        # Header elements
        cls.get_label(image=APP_ICON_IMAGE).pack(padx=20, pady=15)
        cls.set_text(text=i18n.get("records.title"), **page_styles.title)
        cls.set_empty_separator(pady=2)
        cls.set_return_btn()

        # - Page elements:

        records_grid = cls.get_grid()
        navigation_grid = cls.get_grid()

        search_entry = cls.get_entry(records_grid)
        search_button = cls.get_button(records_grid)

        page_indexation = cls.get_label(navigation_grid)
        cls._left_nav_arrow = cls.get_button(navigation_grid)
        cls._right_nav_arrow = cls.get_button(navigation_grid)

        add_record_button = cls.get_button()
        delete_button = cls.get_button()

        # - Elements configuration:

        if cls._last_filter.search_text is not None:
            cls.main_entry = search_entry

        # Grids
        records_grid.pack(fill="both", padx=20, pady=0)
        navigation_grid.pack(fill="none", padx=35, pady=0)

        # Search entry
        search_entry.config(textvariable=cls._filter_var, **app_styles.text_entry)
        search_entry.config(width=30)
        search_entry.grid(row=0, column=1, columnspan=3, padx=0, pady=10, sticky="nsew")
        search_entry.bind(EventType.ESCAPE, lambda event: cls.root.focus_set())
        search_entry.bind(EventType.RETURN, lambda event: search_button.invoke())

        # Search button
        search_button.config(
            text=i18n.get("records.search"),
            command=lambda: cls._on_filter(),
            **page_styles.search_button,
        )
        search_button.grid(row=0, column=4, sticky="w")

        # Page indexation
        page_indexation_text = i18n.get("records.page_indexation").format(
            page_index=cls._page_index, max_page_index=cls._max_page_index
        )
        page_indexation.config(text=page_indexation_text, **page_styles.page_indexation)
        page_indexation.grid(row=0, column=1, padx=0, pady=5, sticky="nsew")

        # Left arrow config
        cls._left_nav_arrow.grid(row=0, column=2, padx=0, pady=5, sticky="nsew")
        cls._left_nav_arrow.config(
            text=LEFT_NAV_ARROW_BUTTON_TEXT,
            command=cls._load_next_page,
            **page_styles.navigation_arrow,
        )
        if cls._page_index >= cls._max_page_index:
            cls._left_nav_arrow.config(state=tk.DISABLED)
        else:
            cls._left_nav_arrow.config(cursor="hand2")

        # Right arrow config
        cls._right_nav_arrow.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        cls._right_nav_arrow.config(
            text=RIGHT_NAV_ARROW_BUTTON_TEXT,
            command=cls._load_prev_page,
            **page_styles.navigation_arrow,
        )
        if cls._page_index <= 1:
            cls._right_nav_arrow.config(state=tk.DISABLED)
        else:
            cls._right_nav_arrow.config(cursor="hand2")

        cls.set_empty_separator(pady=1)

        # Add record button
        add_record_button.config(
            text=ADD_RECORD_BUTTON_EMOJI + " " + i18n.get("records.add_record"),
            command=FormPage.show,
            **page_styles.add_button,
        )
        add_record_button.pack(pady=0)

        # Delete records button
        delete_button.config(
            text=DELETE_RECORDS_BUTTON_EMOJI + " " + i18n.get("records.delete_records"),
            command=cls._on_delete_click,
            **page_styles.delete_all_button,
        )
        delete_button.pack(pady=12)

        cls.set_footer()
        cls._fill_records_grid(records_grid)

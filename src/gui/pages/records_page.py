import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from tkinter import messagebox
from typing import Any, Optional

from common.utils import load_resized_image_tk, path_exists
from gui.assets.images import EMPTY_IMAGE
from models.prediction_model import TagPrediction
from models.record_model import Record
from services.i18n_service import i18n
from services.records_service import RecordsService

from ..assets.images import APP_ICON_IMAGE
from ..page import Page
from ..styles import app as app_styles
from ..styles import records_page as page_styles
from ..tk_enums import EventType, MouseType
from .form_page import FormPage
from .menu_page import MenuPage


class TableIndices(int, Enum):
    MAX_COLUMN_INDEX = 5
    FLOWER_COLUMN_INDEX = 4
    MAX_ROW_INDEX_PER_PAGE = 3


class TableSymbols(str, Enum):
    LEFT_ARROW = ">"
    RIGHT_ARROW = "<"
    ADD_RECORD = "✚"
    DELETE_RECORDS = "✘"
    HIGHEST_FLOWER_PROBABILITY = "✔"
    FAILED_FLOWER_PROBABILITY = "✗"


@dataclass(slots=True)
class SearchFilter:
    search_text: Optional[str] = field(default=None)
    search_column: Optional[str] = field(default=None)

    def reset(self) -> None:
        self.search_text = None
        self.search_column = None


class RecordsPage(Page):
    prev_page = MenuPage

    # Record storage
    _all_records: list[Record]
    _filtered_records: list[Optional[Record]]

    # Filter variables
    _filter_var: tk.StringVar = tk.StringVar()
    _last_filter: SearchFilter = SearchFilter()
    _filter_column_name: str

    # Column variables
    _column_names: tuple[str, ...]
    _column_buttons: list[tk.Button] = []

    # Navigation variables
    _page_index: int = 0
    _max_page_index: int = 0
    _left_nav_arrow: tk.Button
    _right_nav_arrow: tk.Button

    # - Utils:

    @staticmethod
    def _get_arrow_state(enable: bool):
        return tk.NORMAL if enable else tk.DISABLED

    @staticmethod
    def _get_arrow_cursor_state(enable: bool) -> MouseType:
        return MouseType.CAN_CLICK if enable else MouseType.CANT_CLICK

    @classmethod
    def _update_table(cls) -> None:
        cls.reset()
        super().show()

    @classmethod
    def _reload_records(cls) -> None:
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
    def _add_missing_records(cls) -> None:
        cls._filter_records()

        max_record_index = len(cls._filtered_records) - 1
        if max_record_index == -1:
            cls._page_index = 0
            cls._max_page_index = 0
            return

        max_row = TableIndices.MAX_ROW_INDEX_PER_PAGE
        last_page_index, last_page_records_count = divmod(max_record_index, max_row)

        cls._page_index = 1
        cls._max_page_index = last_page_index + 1

        if max_record_index < max_row:
            return

        missing_records = [None] * (max_row - last_page_records_count)
        cls._filtered_records.extend(missing_records)

    # - on_verb methods:

    @classmethod
    def _on_show_prev_page_click(cls) -> None:
        if cls._page_index == 1:
            cls._right_nav_arrow.config(state=tk.DISABLED)
            return

        cls._page_index -= 1
        cls._update_table()

    @classmethod
    def _on_show_next_page_click(cls) -> None:
        if cls._page_index == cls._max_page_index:
            cls._left_nav_arrow.config(state=tk.DISABLED)
            return

        cls._page_index += 1
        cls._update_table()

    @classmethod
    def _on_delete_button_click(cls) -> None:
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
        prev_filter_column = cls._filter_column_name
        if filter_column == prev_filter_column:
            return

        cls._filter_column_name = filter_column

        # Update column buttons
        for col_button in cls._column_buttons:
            button_text = col_button["text"]
            if button_text == filter_column:
                col_button.config(font=page_styles.column_filter_font)
            elif button_text == prev_filter_column:
                col_button.config(font=page_styles.column_font)

    @classmethod
    def _on_search_records(cls) -> None:
        current_filter = SearchFilter(cls._filter_var.get(), cls._filter_column_name)
        if current_filter == cls._last_filter:
            return

        prev_records = cls._filtered_records.copy()
        cls._last_filter = current_filter
        cls._add_missing_records()
        if cls._filtered_records == prev_records:
            return

        cls._update_table()

    @classmethod
    def _on_search_entry_change(cls, *args) -> None:
        current = cls._filter_var.get()
        if current:
            return

        if not cls._last_filter.search_text:
            return

        cls._on_search_records()

    @classmethod
    def _on_classify_record_click(cls, record_id: int) -> None:
        prev_page_index = cls._page_index

        RecordsService.set_record_prediction(record_id)
        cls._reload_records()
        cls._add_missing_records()

        cls._page_index = prev_page_index
        cls._update_table()

    # - Records grid utils:

    @classmethod
    def _get_empty_classification_cell(cls, root: tk.Frame, record_id: int) -> tk.Frame:
        # Cell elements
        grid = cls.get_grid(root)
        label = cls.get_label(grid)
        button = cls.get_button(grid)

        # Elements configuration
        grid.rowconfigure(0, weight=1)
        label.config(**page_styles.empty_prediction_cell_label)
        button.config(
            text=i18n.get("records.classify_button"),
            command=lambda: cls._on_classify_record_click(record_id),
            **page_styles.classify_button,
        )

        # Elements widget configuration
        label.grid(row=0, column=0, pady=5)
        button.grid(row=1, column=0)

        return grid

    @classmethod
    def _insert_inner_classification_cell(
        cls, root: tk.Frame, row: int, col: int, cell_value: str
    ) -> None:
        cell_style = (
            page_styles.top_prediction_cell
            if row == 1
            else page_styles.failed_prediction_cell
        )

        label = cls.get_label(root)
        label.config(text=cell_value, **cell_style)
        label.grid(row=row, column=col, sticky="nsew")

    @classmethod
    def _get_classification_cell(
        cls, root: tk.Frame, predictions: list[TagPrediction]
    ) -> tk.Frame:
        # Cell elements
        grid = cls.get_grid(root)
        tag_label = cls.get_label(grid)
        probability_label = cls.get_label(grid)

        # Elements configuration
        tag_label.config(
            text=i18n.get("records.prediction_tag_column"),
            **page_styles.tag_column_cell,
        )
        probability_label.config(
            text=i18n.get("records.prediction_probability_column"),
            **page_styles.probability_column_cell,
        )

        # Elements widget configuration
        tag_label.grid(row=0, column=0, padx=0, sticky="nsew")
        probability_label.grid(row=0, column=1, padx=0, sticky="nsew")

        # Insert prediction elements
        for row, prediction in enumerate(predictions):
            tag_name = prediction.tag_name.capitalize()
            probability = f"{prediction.probability:.2%} " + (
                TableSymbols.HIGHEST_FLOWER_PROBABILITY
                if row == 0
                else TableSymbols.FAILED_FLOWER_PROBABILITY
            )

            cls._insert_inner_classification_cell(grid, row + 1, 0, tag_name)
            cls._insert_inner_classification_cell(grid, row + 1, 1, probability)

        return grid

    @staticmethod
    def _get_cell_style(row: int, col: int) -> dict[str, Any]:
        if col == 0:
            return {}
        if row == 0:
            return page_styles.column_cell
        if row % 2:
            return page_styles.odd_row_cell

        return page_styles.even_row_cell

    @classmethod
    def _get_cell(
        cls, root: tk.Frame, row: int, col: int, cell_value: str
    ) -> tk.Label | tk.Button:
        # Flower image
        if row > 0 and col == TableIndices.FLOWER_COLUMN_INDEX:
            cell_image = (
                load_resized_image_tk(cell_value)
                if path_exists(cell_value)
                else EMPTY_IMAGE
            )

            return cls.get_label(root, image=cell_image)

        cell_font = page_styles.column_font

        # Label
        if row > 0 or col in (
            0,
            TableIndices.FLOWER_COLUMN_INDEX,
            TableIndices.MAX_COLUMN_INDEX,
        ):
            cell = cls.get_label(root)
            if row > 0:
                cell_font = page_styles.cell_font
                if col > 0:
                    cell.config(cursor=MouseType.READ_TEXT)
        # Button
        else:
            # Underline filter column
            if cell_value == cls._filter_column_name:
                cell_font = page_styles.column_filter_font

            cell = cls.get_button(root)
            cell.config(
                command=lambda: cls._on_column_name_click(cell_value),
                **page_styles.column_button,
            )

            cls._column_buttons.append(cell)

        cell.config(text=cell_value, font=cell_font, relief="flat")

        # First two columns style
        if col not in (0, 1):
            return cell

        cell_style = (
            page_styles.first_column_cell_anchor
            if row == 0
            else (
                page_styles.index_cell_column_anchor
                if col == 0
                else page_styles.uploaded_by_cell_column_anchor
            )
        )

        cell.config(**cell_style)
        return cell

    @classmethod
    def _fill_records_grid(cls, grid: tk.Frame) -> None:
        cls._column_buttons = []
        max_row = TableIndices.MAX_ROW_INDEX_PER_PAGE
        first_record_index = max(0, max_row * (cls._page_index - 1))
        last_record_index = min(
            first_record_index + max_row,
            len(cls._filtered_records) - 1,
        )

        record_indices = range(first_record_index - 1, last_record_index + 1)
        for row, record_index in enumerate(record_indices):
            if row == max_row + 1:
                break

            # Get row cells
            insert_empty_row = False
            if row == 0:
                raw_row_cells = cls._column_names
            else:
                record = cls._filtered_records[record_index]
                record_id = record.record_id if isinstance(record, Record) else -1
                if record is None:
                    insert_empty_row = True
                    raw_row_cells = tuple(
                        None for _ in range(TableIndices.MAX_COLUMN_INDEX + 1)
                    )
                else:
                    raw_row_cells = (
                        f"{record_id + 1}.",
                        record.name,
                        record.surname,
                        record.address,
                        record.image_path,
                        record.predictions,
                    )

            # Insert grid row
            for col, cell_value in enumerate(raw_row_cells):
                # Insert empty cell
                if insert_empty_row:
                    if col == TableIndices.FLOWER_COLUMN_INDEX:
                        cell = cls.get_label(grid, EMPTY_IMAGE)
                    else:
                        cell = cls.get_label(grid)

                # Insert empty flower clarification cell
                elif cell_value is None:
                    cell = cls._get_empty_classification_cell(grid, record_id)
                    cell.grid(row=row + 1, column=col, padx=0, pady=1)
                    continue

                # Insert flower clarification cell
                elif isinstance(cell_value, list):
                    sorted_predictions = sorted(cell_value, reverse=True)
                    cell = cls._get_classification_cell(grid, sorted_predictions)
                    cell.grid(row=row + 1, column=col)
                    continue

                # Insert a button/label
                else:
                    cell = cls._get_cell(grid, row, col, cell_value)
                    cell.config(**cls._get_cell_style(row, col))

                cell.grid(row=row + 1, column=col, padx=0, pady=1, sticky="nsew")

    # - Overridden methods:

    @classmethod
    def close(cls) -> None:
        cls.main_entry = None
        cls._filter_var.set("")
        cls._last_filter.reset()

    @classmethod
    def show(cls) -> None:
        FormPage.prev_page = cls

        # Update language data
        cls._filter_column_name: str = i18n.get("records.owner_column")
        cls._column_names = (
            "",  # Record index column
            i18n.get("records.owner_column"),
            i18n.get("records.surname_column"),
            i18n.get("records.address_column"),
            i18n.get("records.flower_column"),
            i18n.get("records.prediction_column"),
        )

        cls._reload_records()
        cls._add_missing_records()
        cls._update_table()

    @classmethod
    def load(cls) -> None:
        # - Page elements:

        app_icon = cls.get_label(image=APP_ICON_IMAGE)

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

        search_entry.config(textvariable=cls._filter_var, **app_styles.text_entry)
        search_button.config(
            text=i18n.get("records.search"),
            command=lambda: cls._on_search_records(),
            **page_styles.search_button,
        )

        right_enabled = cls._page_index > 1
        left_enabled = cls._page_index < cls._max_page_index
        page_indexation.config(
            text=i18n.get("records.page_indexation").format(
                page_index=cls._page_index, max_page_index=cls._max_page_index
            ),
            **page_styles.page_indexation,
        )
        cls._left_nav_arrow.config(
            text=TableSymbols.LEFT_ARROW,
            command=cls._on_show_next_page_click,
            state=cls._get_arrow_state(left_enabled),
            cursor=cls._get_arrow_cursor_state(left_enabled),
            **page_styles.navigation_arrow,
        )
        cls._right_nav_arrow.config(
            text=TableSymbols.RIGHT_ARROW,
            command=cls._on_show_prev_page_click,
            state=cls._get_arrow_state(right_enabled),
            cursor=cls._get_arrow_cursor_state(right_enabled),
            **page_styles.navigation_arrow,
        )

        add_record_button.config(
            text=TableSymbols.ADD_RECORD + " " + i18n.get("records.add_record"),
            command=FormPage.show,
            **page_styles.add_button,
        )
        delete_button.config(
            text=TableSymbols.DELETE_RECORDS + " " + i18n.get("records.delete_records"),
            command=cls._on_delete_button_click,
            **page_styles.delete_all_button,
        )

        # Elements bindings configuration
        search_entry.bind(EventType.ESCAPE, lambda event: cls.root.focus_set())
        search_entry.bind(EventType.RETURN, lambda event: cls._on_search_records())
        cls._filter_var.trace_add(
            "write", lambda *args: cls._on_search_entry_change(args)
        )

        # - Elements widget configuration:

        cls.set_return_button()

        # Header
        app_icon.pack(padx=20, pady=15)
        cls.set_text(text=i18n.get("records.title"), **app_styles.page_title)
        cls.set_empty_separator(pady=2)

        # Grids
        records_grid.pack(fill="both", padx=20, pady=0)
        navigation_grid.pack(fill="none", padx=35, pady=0)

        # Search
        search_button.grid(row=0, column=4, sticky="w")
        search_entry.grid(row=0, column=1, columnspan=3, padx=0, pady=10, sticky="nsew")

        # Navigation
        page_indexation.grid(row=0, column=1, padx=0, pady=5, sticky="nsew")
        cls._right_nav_arrow.grid(row=0, column=0, padx=0, pady=5, sticky="nsew")
        cls._left_nav_arrow.grid(row=0, column=2, padx=0, pady=5, sticky="nsew")
        cls.set_empty_separator(pady=1)

        # Buttons
        add_record_button.pack(pady=0)
        delete_button.pack(pady=12)

        cls.set_copyright()
        cls._fill_records_grid(records_grid)

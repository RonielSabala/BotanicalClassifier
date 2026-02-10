"""
Displays saved records in a paginated, filterable table with
image previews and optional classification results.
"""

import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from tkinter import messagebox
from typing import Any, Optional

from common.utils import load_resized_image_tk, path_exists
from models import Record, TagPrediction
from services import RecordsService, i18n

from ..assets import APP_ICON_IMAGE, EMPTY_IMAGE
from ..page import Page
from ..styles import app as app_styles, records_page as page_styles
from ..tk_enums import BindingKey, CursorType
from .form_page import FormPage
from .menu_page import MenuPage

COLUMN_NAMES: tuple[str, ...] = ()


def _update_column_names() -> None:
    """
    Update table columns names.
    """

    global COLUMN_NAMES
    COLUMN_NAMES = (
        "",  # <- Record index column
        i18n.get("records.owner_column"),
        i18n.get("records.surname_column"),
        i18n.get("records.address_column"),
        i18n.get("records.flower_column"),
        i18n.get("records.prediction_column"),
    )


class TableLayout(int, Enum):
    COLUMNS = 6
    ROWS_PER_PAGE = 3
    FLOWER_COLUMN = 5
    SEARCH_ENTRY_COLUMNSPAN = 3


@dataclass(slots=True)
class SearchFilter:
    text: Optional[str] = field(default=None)
    column: Optional[str] = field(default=None)

    def is_active(self) -> bool:
        """
        Whether `text` is not empty.
        """

        return self.text is not None and self.text != ""

    def reset(self) -> None:
        """
        Set both `text` and `column` to None.
        """

        self.text = None
        self.column = None


class UISymbols(str, Enum):
    PREV_PAGE = "<"
    NEXT_PAGE = ">"
    ADD_RECORD = "✚"
    DELETE_RECORDS = "✘"
    SUCCESS = "✔"
    FAILURE = "✗"


class RecordsPage(Page):
    prev_page = MenuPage

    _all_records: list[Record]
    _visible_records: list[Optional[Record]]

    _page_index: int = 0
    _max_page_index: int = 0

    _filter: SearchFilter = SearchFilter()
    _filter_var: tk.StringVar = tk.StringVar()

    _column_names: tuple[str, ...]
    _column_buttons: list[tk.Button] = []
    _active_filter_column: str

    _left_arrow: tk.Button
    _right_arrow: tk.Button

    # - Data helpers:

    @classmethod
    def _reload_records(cls) -> None:
        cls._all_records = list(RecordsService.iter_records())

    @classmethod
    def _apply_filter(cls) -> list[Record]:
        if not cls._filter.is_active():
            return cls._all_records.copy()

        text_to_filter = cls._filter_var.get().lower()
        filter_column_index = COLUMN_NAMES.index(cls._active_filter_column) - 1

        result: list[Record] = []
        for record in cls._all_records:
            record_property = record.get_property_by_index(filter_column_index)
            if text_to_filter not in record_property.lower():
                continue

            result.append(record)

        return result

    @classmethod
    def _paginate(cls) -> None:
        cls._visible_records = cls._apply_filter()  # type: ignore

        max_record_index = len(cls._visible_records) - 1
        if max_record_index == -1:
            cls._page_index = 0
            cls._max_page_index = 0
            return

        max_row = TableLayout.ROWS_PER_PAGE
        last_page_index, last_page_records_count = divmod(max_record_index, max_row)

        cls._page_index = 1
        cls._max_page_index = last_page_index + 1

        if max_record_index < max_row:
            return

        missing_records = [None] * (max_row - last_page_records_count)
        cls._visible_records.extend(missing_records)

    # - Event handlers:

    @classmethod
    def _on_prev_page(cls) -> None:
        if cls._page_index == 1:
            return

        cls._page_index -= 1
        cls._update_table()

    @classmethod
    def _on_next_page(cls) -> None:
        if cls._page_index == cls._max_page_index:
            return

        cls._page_index += 1
        cls._update_table()

    @classmethod
    def _on_delete_all(cls) -> None:
        if not cls._all_records:
            return

        if not messagebox.askyesno(
            i18n.get("records.delete_dialog_title"),
            i18n.get("records.delete_dialog_text"),
        ):
            return

        RecordsService.delete_all_records()
        MenuPage.show()

    @classmethod
    def _on_column_click(cls, column: str) -> None:
        prev_filter_column = cls._active_filter_column
        if column == prev_filter_column:
            return

        cls._active_filter_column = column

        # Update column buttons style
        for col_button in cls._column_buttons:
            button_text = col_button["text"]
            if button_text == column:
                col_button.config(font=page_styles.column_filter_font)
            elif button_text == prev_filter_column:
                col_button.config(font=page_styles.column_font)

    @classmethod
    def _on_search(cls) -> None:
        active_filter = SearchFilter(cls._filter_var.get(), cls._active_filter_column)
        if active_filter == cls._filter:
            return

        prev_records = cls._visible_records.copy()
        cls._filter = active_filter
        cls._paginate()
        if cls._visible_records == prev_records:
            return

        cls._update_table()

    @classmethod
    def _on_search_entry(cls, *args) -> None:
        current = cls._filter_var.get()
        if current:
            return

        if not cls._filter.is_active():
            return

        cls._on_search()

    @classmethod
    def _on_classify(cls, record_id: int) -> None:
        prev_page_index = cls._page_index

        RecordsService.set_record_prediction(record_id)
        cls._reload_records()
        cls._paginate()

        cls._page_index = prev_page_index
        cls._update_table()

    # - UI helpers:

    @staticmethod
    def _get_cell_style(row: int, col: int) -> dict[str, Any]:
        if col == 0:
            return {}
        if row == 0:
            return page_styles.column_cell
        if row % 2:
            return page_styles.odd_row_cell

        return page_styles.even_row_cell

    @staticmethod
    def _get_arrow_state(enable: bool) -> dict[str, Any]:
        state = tk.NORMAL if enable else tk.DISABLED
        cursor = CursorType.CAN_CLICK if enable else CursorType.CANT_CLICK
        return {"state": state, "cursor": cursor}

    # - Grid rendering:

    @classmethod
    def _get_empty_prediction_cell(cls, root: tk.Frame, record_id: int) -> tk.Frame:
        # Cell widgets
        grid = cls.get_grid(root)
        label = cls.get_label(grid)
        button = cls.get_button(grid)

        # Configuration
        grid.rowconfigure(0, weight=1)
        label.config(**page_styles.empty_prediction_cell_label)
        button.config(
            text=i18n.get("records.classify_button"),
            command=lambda: cls._on_classify(record_id),
            **page_styles.classify_button,
        )

        # Layout
        label.grid(row=0, column=0)
        button.grid(row=1, column=0)
        return grid

    @classmethod
    def _insert_inner_prediction_cell(
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
    def _get_prediction_cell(
        cls, root: tk.Frame, predictions: list[TagPrediction]
    ) -> tk.Frame:
        # Cell widgets
        grid = cls.get_grid(root)
        tag_label = cls.get_label(grid)
        probability_label = cls.get_label(grid)

        # Configuration
        tag_label.config(
            text=i18n.get("records.prediction_tag_column"),
            **page_styles.tag_column_cell,
        )
        probability_label.config(
            text=i18n.get("records.prediction_probability_column"),
            **page_styles.probability_column_cell,
        )

        # Layout
        tag_label.grid(row=0, column=0, sticky="nsew")
        probability_label.grid(row=0, column=1, sticky="nsew")

        # Insert prediction elements
        for row, prediction in enumerate(predictions):
            tag_name = prediction.tag_name.capitalize()
            probability = f"{prediction.probability:.2%} " + (
                UISymbols.SUCCESS if row == 0 else UISymbols.FAILURE
            )

            cls._insert_inner_prediction_cell(grid, row + 1, 0, tag_name)
            cls._insert_inner_prediction_cell(grid, row + 1, 1, probability)

        return grid

    @classmethod
    def _get_cell(
        cls, root: tk.Frame, row: int, col: int, cell_value: str
    ) -> tk.Label | tk.Button:
        # Flower image
        flower_column_index = TableLayout.FLOWER_COLUMN - 1
        if row > 0 and col == flower_column_index:
            cell_image = (
                load_resized_image_tk(cell_value)
                if path_exists(cell_value)
                else EMPTY_IMAGE
            )

            return cls.get_label(root, image=cell_image)

        cell_font = page_styles.column_font

        # Label
        if row > 0 or col in (0, flower_column_index, TableLayout.COLUMNS - 1):
            cell = cls.get_label(root)
            if row > 0:
                cell_font = page_styles.cell_font
                if col > 0:
                    cell.config(cursor=CursorType.READ_TEXT)
        # Button
        else:
            # Underline filter column
            if cell_value == cls._active_filter_column:
                cell_font = page_styles.column_filter_font

            cell = cls.get_button(root)
            cell.config(
                command=lambda: cls._on_column_click(cell_value),
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
    def _render_records_grid(cls, grid: tk.Frame) -> None:
        cls._column_buttons = []
        max_row = TableLayout.ROWS_PER_PAGE
        flow_column_index = TableLayout.FLOWER_COLUMN - 1

        start_record_index = max(0, max_row * (cls._page_index - 1))
        end_record_index = min(
            start_record_index + max_row, len(cls._visible_records) - 1
        )

        record_indices = range(start_record_index - 1, end_record_index + 1)
        for row, record_index in enumerate(record_indices):
            if row == max_row + 1:
                break

            # Get row cells
            record_id = -1
            insert_empty_row = False
            if row == 0:
                row_cells = COLUMN_NAMES
            else:
                record = cls._visible_records[record_index]
                record_id = record.record_id if isinstance(record, Record) else -1
                if record is None:
                    insert_empty_row = True
                    row_cells = tuple(None for _ in range(TableLayout.COLUMNS))
                else:
                    row_cells = (
                        f"{record_id + 1}.",
                        record.name,
                        record.surname,
                        record.address,
                        record.image_path,
                        record.predictions,
                    )

            # Insert grid row
            for col, cell_value in enumerate(row_cells):
                # Insert empty cell
                if insert_empty_row:
                    cell = (
                        cls.get_label(grid, EMPTY_IMAGE)
                        if col == flow_column_index
                        else cls.get_label(grid)
                    )

                    cell.grid(pady=1, sticky="nsew")

                # Insert empty flower prediction cell
                elif cell_value is None:
                    cell = cls._get_empty_prediction_cell(grid, record_id)

                # Insert flower prediction cell
                elif isinstance(cell_value, list):
                    sorted_predictions = sorted(cell_value, reverse=True)
                    cell = cls._get_prediction_cell(grid, sorted_predictions)

                # Insert a button/label
                else:
                    cell = cls._get_cell(grid, row, col, cell_value)
                    cell.config(**cls._get_cell_style(row, col))
                    cell.grid(pady=1, sticky="nsew")

                cell.grid(row=row + 1, column=col)

    # - Page lifecycle:

    @classmethod
    def _update_table(cls) -> None:
        cls.reset()
        super().show()

    @classmethod
    def close(cls) -> None:
        cls.main_entry = None
        cls._filter_var.set("")
        cls._filter.reset()

    @classmethod
    def show(cls) -> None:
        FormPage.prev_page = cls

        # Update language data
        cls._active_filter_column = i18n.get("records.owner_column")
        _update_column_names()

        cls._reload_records()
        cls._paginate()
        cls._update_table()

    @classmethod
    def load(cls) -> None:
        # - Widgets:

        app_icon = cls.get_label(image=APP_ICON_IMAGE)
        records_grid = cls.get_grid()
        nav_grid = cls.get_grid()

        search_entry = cls.get_entry(records_grid)
        search_button = cls.get_button(records_grid)

        page_label = cls.get_label(nav_grid)
        cls._left_arrow = cls.get_button(nav_grid)
        cls._right_arrow = cls.get_button(nav_grid)

        add_button = cls.get_button()
        delete_button = cls.get_button()

        # - Configuration:

        if cls._filter.text is not None:
            cls.main_entry = search_entry

        search_entry.config(textvariable=cls._filter_var, **app_styles.text_entry)
        search_button.config(
            text=i18n.get("records.search"),
            command=lambda: cls._on_search(),
            **page_styles.search_button,
        )

        page_label.config(
            text=i18n.get("records.page_indexation").format(
                page_index=cls._page_index, max_page_index=cls._max_page_index
            ),
            **page_styles.page_indexation,
        )

        left_enabled = cls._page_index > 1
        cls._left_arrow.config(
            text=UISymbols.PREV_PAGE,
            command=cls._on_prev_page,
            **cls._get_arrow_state(left_enabled),
            **page_styles.navigation_arrow,
        )

        right_enabled = cls._page_index < cls._max_page_index
        cls._right_arrow.config(
            text=UISymbols.NEXT_PAGE,
            command=cls._on_next_page,
            **cls._get_arrow_state(right_enabled),
            **page_styles.navigation_arrow,
        )

        add_button.config(
            text=UISymbols.ADD_RECORD + " " + i18n.get("records.add_record"),
            command=FormPage.show,
            **page_styles.add_button,
        )
        delete_button.config(
            text=UISymbols.DELETE_RECORDS + " " + i18n.get("records.delete_records"),
            command=cls._on_delete_all,
            **page_styles.delete_all_button,
        )

        # Bindings
        search_entry.bind(BindingKey.RETURN, lambda _: cls._on_search())
        search_entry.bind(BindingKey.ESCAPE, lambda _: cls.root.focus_set())
        cls._filter_var.trace_add("write", lambda *args: cls._on_search_entry(args))

        # - Layout:

        cls.set_return_button()

        app_icon.pack(padx=20, pady=15)
        cls.set_text(text=i18n.get("records.title"), **app_styles.page_title)

        cls.set_empty_separator(pady=2)

        records_grid.pack(fill="both", padx=20, pady=0)
        nav_grid.pack(fill="none", padx=35, pady=0)

        columnspan = TableLayout.SEARCH_ENTRY_COLUMNSPAN.value
        search_entry.grid(
            row=0, column=1, columnspan=columnspan, pady=10, sticky="nsew"
        )
        search_button.grid(row=0, column=columnspan + 1, sticky="w")

        cls._left_arrow.grid(row=0, column=0, pady=5, sticky="nsew")
        page_label.grid(row=0, column=1, pady=5, sticky="nsew")
        cls._right_arrow.grid(row=0, column=2, pady=5, sticky="nsew")

        cls.set_empty_separator(pady=1)

        add_button.pack(pady=0)
        delete_button.pack(pady=12)

        cls.set_copyright()
        cls._render_records_grid(records_grid)

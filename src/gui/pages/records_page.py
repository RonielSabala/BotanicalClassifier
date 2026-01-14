import tkinter as tk
from tkinter import Frame, font, messagebox
from typing import Optional

from common.utils import is_valid_path
from gui.assets.images import EMPTY_IMAGE, get_resized_image
from models.prediction_model import Prediction
from models.record_model import Record
from models.search_filter_model import SearchFilter
from services.i18n_service import i18n
from services.pages.records_service import RecordsService

from ..assets.images import APP_ICON_IMAGE
from ..page import Page
from ..styles import (
    add_button_style,
    delete_button_style,
    entry_text_style,
    navigation_arrow_style,
    primary_button_style,
)
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
UNCLASSIFIED_RECORD_VALUE = "N/A"


class RecordsPage(Page):
    prev_page = MenuPage

    # Records variables
    _all_records: list[tuple[int, Record]]
    _filtered_records: list[tuple[int, Optional[Record]]]
    _filter_var: tk.StringVar = tk.StringVar()
    _last_filter: SearchFilter = SearchFilter()

    # Columns variables
    _column_names: tuple[str, ...]
    _column_buttons: list[tk.Button] = []
    _filter_column_name: str = i18n.get("records.owner_column")
    _max_column_index: int = -1
    _flower_column_index: int = -1

    # Navigation variables
    _page_index: int = -1
    _max_page_index: int = -1
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
        flower_column_name = i18n.get("records.flower_column")
        cls._column_names = (
            "",  # Record index column
            i18n.get("records.owner_column"),
            i18n.get("records.surname_column"),
            i18n.get("records.address_column"),
            flower_column_name,
            i18n.get("records.prediction_column"),
        )

        cls._max_column_index = len(cls._column_names) - 1
        cls._flower_column_index = cls._column_names.index(flower_column_name)

    @classmethod
    def _fill_records(cls) -> None:
        cls._all_records = list(enumerate(RecordsService.get_all_records(), start=1))

    @classmethod
    def _filter_records(cls) -> None:
        if cls._last_filter.search_text is None:
            cls._filtered_records = cls._all_records.copy()  # type: ignore
            return

        text_to_filter = cls._filter_var.get().lower()
        filter_column_index = cls._column_names.index(cls._filter_column_name)
        cls._filtered_records = [
            (i, record)
            for i, record in cls._all_records
            if text_to_filter
            in str(record.get_property_by_index(filter_column_index)).lower()
        ]

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

        missing_records = [(-1, None)] * (
            MAX_ROW_INDEX_PER_PAGE - last_page_records_count
        )

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

        # Update column buttons
        for col_button in cls._column_buttons:
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
    def _classify_record(cls, record_index: int) -> None:
        prev_page_index = cls._page_index

        RecordsService.set_record_prediction(record_index)
        cls._fill_records()
        cls._update_records()

        cls._page_index = prev_page_index
        cls._update_table()

    @classmethod
    def _get_classification_button(cls, root: Frame, record_index: int) -> Frame:
        bg_color = "white"
        grid = Frame(root, bg=bg_color)
        grid.rowconfigure(0, weight=1)
        tk.Label(
            grid,
            text=UNCLASSIFIED_RECORD_VALUE,
            font=("Arial", 13),
            bg=bg_color,
        ).grid(row=0, column=0, pady=5)

        # Create button
        button = tk.Button(
            grid,
            text=i18n.get("records.classify_button"),
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
    def _insert_prediction_cell_element(
        cls, root: Frame, row: int, column: int, cell_value: str
    ) -> None:
        fg_color = "Black" if row == 0 else f"Gray{50 + 8 * row}"
        bg_color = "GoldenRod1" if row == 0 else "White"

        tk.Label(
            root, text=cell_value, font=("Arial", 10), fg=fg_color, bg=bg_color
        ).grid(row=row, column=column, sticky="nsew")

    @classmethod
    def _get_prediction_grid(cls, root: Frame, predictions: list[Prediction]) -> Frame:
        grid = Frame(root)
        prediction_column_names = (
            i18n.get("records.prediction_tag_column"),
            i18n.get("records.prediction_probability_column"),
        )

        # Insert columns names
        for col, column_name in enumerate(prediction_column_names):
            fg_color = "White" if col == 0 else "GoldenRod1"
            font_size = 12 if col == 0 else 10
            label_font = "Arial", font_size, "bold"

            tk.Label(
                grid, text=column_name, font=label_font, fg=fg_color, bg="Gray15"
            ).grid(row=0, column=col, sticky="nsew", padx=0)

        # Insert predictions
        for row, prediction in enumerate(predictions):
            tag_name = prediction.tag_name.capitalize()
            probability = f"{prediction.probability:.2%} " + (
                HIGHEST_FLOWER_PROBABILITY_EMOJI
                if row == 0
                else FAILED_FLOWER_PROBABILITY_EMOJI
            )

            cls._insert_prediction_cell_element(grid, row + 1, 0, tag_name)
            cls._insert_prediction_cell_element(grid, row + 1, 1, probability)

        return grid

    @classmethod
    def _get_cell_colors(cls, row: int, col: int) -> tuple[str, str]:
        fg_color, bg_color = "Black", cls.bg_color
        if col == 0:
            return fg_color, bg_color

        if row == 0:
            # Column colors
            fg_color, bg_color = "white", "Dodgerblue4"
        else:
            # Row colors
            bg_color = "Gray96" if row % 2 else "Gray92"

        return fg_color, bg_color

    @classmethod
    def _get_cell_element(
        cls, root: Frame, row: int, col: int, cell_value: str
    ) -> tk.Label | tk.Button:
        # Flower image
        if row > 0 and col == cls._flower_column_index:
            image = (
                get_resized_image(cell_value)
                if is_valid_path(cell_value)
                else EMPTY_IMAGE
            )

            cell_image = tk.Label(root, image=image)
            cell_image.image = image  # type: ignore
            return cell_image

        # Label
        element_font = "Arial", 16, "bold"
        if row > 0 or col in (0, cls._flower_column_index, cls._max_column_index):
            element = tk.Label(root)
            if row > 0:
                element_font = "Segoe UI Emoji", 13
                if col > 0:
                    element.config(cursor="xterm")

        # Button
        else:
            # Underline filter column
            if cell_value == cls._filter_column_name:
                element_font += ("underline",)

            element = tk.Button(
                root,
                border=0,
                activeforeground="Black",
                activebackground="DodgerBlue4",
                cursor="hand2",
                command=lambda value=cell_value: cls._on_column_name_click(value),
            )

            cls._column_buttons.append(element)

        element.config(text=cell_value, font=element_font, relief="flat")
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

            if row == 0:
                row_data = cls._column_names
            else:
                record_position, record = cls._filtered_records[record_index]

                # Insert empty row
                if record is None:
                    for col in range(cls._max_column_index + 1):
                        tk.Label(grid, text="", bg=cls.bg_color).grid(
                            row=row + 1, column=col, sticky="nsew", pady=1
                        )

                    continue

                row_data = (
                    f"{record_position}.",
                    record.name,
                    record.surname,
                    record.address,
                    record.image_path,
                    record.predictions,
                )

            for col, cell_value in enumerate(row_data):
                # Insert classification button
                if cell_value is None:
                    button = cls._get_classification_button(grid, record_position - 1)
                    button.grid(row=row + 1, column=col, padx=0, pady=1)
                    continue

                # Insert predictions grid
                if isinstance(cell_value, list):
                    sorted_predictions = sorted(
                        cell_value,
                        key=lambda prediction: prediction.probability,
                        reverse=True,
                    )

                    predictions_grid = cls._get_prediction_grid(
                        grid, sorted_predictions
                    )

                    predictions_grid.config(bg=cls.bg_color)
                    predictions_grid.grid(row=row + 1, column=col)
                    continue

                fg_color, bg_color = cls._get_cell_colors(row, col)
                cell_element = cls._get_cell_element(grid, row, col, cell_value)
                cell_element.config(fg=fg_color, bg=bg_color)  # type: ignore
                cell_element.grid(row=row + 1, column=col, sticky="nsew", pady=1)

    @classmethod
    def load(cls) -> None:
        # Header elements
        page_title = i18n.get("records.title")
        tk.Label(cls.root, image=APP_ICON_IMAGE, bg=cls.bg_color).pack(padx=20, pady=15)
        cls.set_text(page_title, 32, pady=0, fg="#091518")
        cls.set_text("", 0, pady=2)
        cls.set_return_btn()

        # - Page elements:

        records_grid = cls.get_grid_from_root()
        navigation_grid = cls.get_grid_from_root()

        search_entry = tk.Entry(
            records_grid, textvariable=cls._filter_var, **entry_text_style
        )

        search_button = tk.Button(
            records_grid,
            text=i18n.get("records.search"),
            font=("Arial", 13),
            command=lambda: cls._on_filter(),
            cursor="hand2",
        )

        cls._left_nav_arrow = tk.Button(
            navigation_grid,
            text=LEFT_NAV_ARROW_BUTTON_TEXT,
            command=cls._load_next_page,
            font=("Arial", 24),
            **navigation_arrow_style,
        )

        cls._right_nav_arrow = tk.Button(
            navigation_grid,
            text=RIGHT_NAV_ARROW_BUTTON_TEXT,
            command=cls._load_prev_page,
            font=("Arial", 24),
            **navigation_arrow_style,
        )

        page_number_label = tk.Label(
            navigation_grid,
            text=i18n.get("records.page_index_label").format(
                page_index=cls._page_index, max_page_index=cls._max_page_index
            ),
            fg="Black",
            bg=cls.bg_color,
            font=("Arial", 14),
        )

        add_record_button_text = (
            ADD_RECORD_BUTTON_EMOJI + " " + i18n.get("records.add_record")
        )

        add_record_button = tk.Button(
            cls.root,
            text=add_record_button_text,
            command=FormPage.show,
            **add_button_style,  # type: ignore
        )

        delete_button_text = (
            DELETE_RECORDS_BUTTON_EMOJI + " " + i18n.get("records.delete_records")
        )

        delete_button = tk.Button(
            cls.root,
            text=delete_button_text,
            command=cls._on_delete_click,
            **delete_button_style,  # type: ignore
        )

        # - Elements configuration:

        if cls._last_filter.search_text is not None:
            cls.main_entry = search_entry

        records_grid.pack(fill="both", padx=20, pady=0)
        navigation_grid.pack(fill="none", padx=35, pady=0)

        search_entry.config(width=30)
        search_entry.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=10)
        search_entry.bind("<Escape>", lambda event: cls.root.focus_set())
        search_entry.bind("<Return>", lambda event: search_button.invoke())

        search_button.grid(row=0, column=4, sticky="w")

        page_number_label.grid(row=0, column=1, sticky="nsew", padx=0, pady=5)
        cls._left_nav_arrow.grid(row=0, column=2, sticky="nsew", padx=0, pady=5)
        cls._right_nav_arrow.grid(row=0, column=0, sticky="nsew", padx=0, pady=5)

        # Left arrow state config
        if cls._page_index >= cls._max_page_index:
            cls._left_nav_arrow.config(state=tk.DISABLED)
        else:
            cls._left_nav_arrow.config(cursor="hand2")

        # Right arrow state config
        if cls._page_index <= 1:
            cls._right_nav_arrow.config(state=tk.DISABLED)
        else:
            cls._right_nav_arrow.config(cursor="hand2")

        cls.set_text("", 0, pady=1)
        add_record_button.pack(pady=0)
        delete_button.pack(pady=12)

        cls.set_footer()
        cls._fill_records_grid(records_grid)

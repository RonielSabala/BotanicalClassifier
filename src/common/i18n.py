import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

from common.constants import I18N_DIR

from .utils import is_valid_path


class Language(str, Enum):
    EN = "en"
    ES = "es"

    @staticmethod
    def all_languages() -> tuple[str, ...]:
        return tuple(member.value for member in Language)


@dataclass(slots=True)
class I18n:
    """
    Lightweight i18n loader using JSON files.
    """

    default: Language
    _current: Language = field(init=False)
    _catalogs: Dict[str, Dict[str, str]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self._current = self.default

        # Load languages
        for lang in Language.all_languages():
            lang_path = f"{I18N_DIR}{lang}.json"
            if not is_valid_path(lang_path):
                raise FileNotFoundError(f"Translation file not found: {lang_path}")

            with open(lang_path, "r", encoding="utf-8") as lang_file:
                lang_json = json.load(lang_file)

            self._catalogs[lang] = {str(k): str(v) for k, v in lang_json.items()}

    def set_language(self, lang: Language) -> None:
        """
        Cambia el idioma actual.
        """

        self._current = lang

    def get(self, key: str) -> str:
        catalog = self._catalogs[self._current]
        value = catalog.get(key)
        if value is None:
            return key

        return value


# Global singleton
i18n = I18n(default=Language.EN)

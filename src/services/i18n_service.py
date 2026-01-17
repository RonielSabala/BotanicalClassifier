"""
i18n service that loads simple JSON translation catalogs
per language code.
"""

import json
from dataclasses import dataclass, field
from enum import Enum

from common.paths import i18n_file_path
from common.utils import path_exists


class Language(str, Enum):
    EN = "en"
    ES = "es"

    @staticmethod
    def all_languages() -> tuple[str, ...]:
        """
        Return a tuple of all supported language codes.
        """

        return tuple(member.value for member in Language)


@dataclass(slots=True)
class I18nService:
    """
    Lightweight i18n loader backed by JSON files.
    """

    default: Language
    _current: str = field(init=False)
    _catalogs: dict[str, dict[str, str]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.set_language(self.default.value)

    def _add_language(self, lang: str) -> None:
        """
        Load the language file to store it in the catalog.
        Raises FileNotFoundError if the translation file
        does not exist.
        """

        lang_file = i18n_file_path(lang)
        if not path_exists(lang_file):
            raise FileNotFoundError(f"Translation file not found: {lang_file}")

        with open(lang_file, "r", encoding="utf-8") as f:
            lang_json = json.load(f)

        self._catalogs[lang] = {str(k): str(v) for k, v in lang_json.items()}

    def set_language(self, lang: str) -> None:
        """
        Set `lang` as the current language.
        """

        self._current = lang
        if lang not in self._catalogs:
            self._add_language(lang)

    @property
    def current_language(self) -> str:
        """
        Current language code.
        """

        return self._current

    def get(self, key: str) -> str:
        """
        Fetch translated string for `key`. If the catalog
        is not loaded or the key is missing, returns `key`.
        """

        catalog = self._catalogs[self._current]
        value = catalog.get(key)
        if value is None:
            return key

        return value


# Global singleton
i18n = I18nService(default=Language.EN)

# Public API
__all__ = ("Language", "i18n")

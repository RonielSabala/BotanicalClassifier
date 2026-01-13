import json
from dataclasses import dataclass, field
from enum import Enum

from common.constants import I18N_DIR
from common.utils import is_valid_path


class Language(str, Enum):
    EN = "en"
    ES = "es"

    @staticmethod
    def all_languages() -> tuple[str, ...]:
        return tuple(member.value for member in Language)


@dataclass(slots=True)
class I18nService:
    """
    Lightweight i18n loader using JSON files.
    """

    default: Language
    _current: Language = field(init=False)
    _catalogs: dict[str, dict[str, str]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.set_language(self.default)

    def set_language(self, lang: Language) -> None:
        lang_path = f"{I18N_DIR}/{lang.value}.json"
        if not is_valid_path(lang_path):
            raise FileNotFoundError(f"Translation file not found: {lang_path}")

        with open(lang_path, "r", encoding="utf-8") as lang_file:
            lang_json = json.load(lang_file)

        self._current = lang
        self._catalogs[lang] = {str(k): str(v) for k, v in lang_json.items()}

    @property
    def current_language(self) -> str:
        return self._current.value

    def get(self, key: str) -> str:
        catalog = self._catalogs[self._current]
        value = catalog.get(key)
        if value is None:
            return key

        return value


# Global singleton
i18n = I18nService(default=Language.EN)

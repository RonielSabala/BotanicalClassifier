"""
Service to load localized static content.
"""

from pathlib import Path
from typing import Callable

from common.paths import faq_path, policies_path, terms_path

from .i18n_service import i18n


class AboutService:
    @staticmethod
    def _load_page(path_getter: Callable[[str], Path]) -> str:
        """
        Load and return the content for the page determined by
        `path_getter`.

        * Parameters:
            - path_getter: Callable that receives a language code
            and returns a Path to the content file.
        """

        lang_code = i18n.current_language
        file_path = path_getter(lang_code)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def get_faq(cls) -> str:
        """
        Return FAQ content for the current language.
        """

        return cls._load_page(faq_path)

    @classmethod
    def get_terms(cls) -> str:
        """
        Return Terms content for the current language.
        """

        return cls._load_page(terms_path)

    @classmethod
    def get_policies(cls) -> str:
        """
        Return Policies content for the current language.
        """

        return cls._load_page(policies_path)


# Public API
__all__ = ("AboutService",)

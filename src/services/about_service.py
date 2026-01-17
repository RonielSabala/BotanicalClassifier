from pathlib import Path
from typing import Callable

from common.paths import faq_path, policies_path, terms_path

from .i18n_service import i18n


class AboutService:
    @staticmethod
    def _get_page_content(path_getter: Callable[[str], Path]) -> str:
        with open(path_getter(i18n.current_language), "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def get_faq(cls) -> str:
        """
        Return the FAQ text file.
        """

        return cls._get_page_content(faq_path)

    @classmethod
    def get_terms(cls) -> str:
        """
        Return the Terms text file.
        """

        return cls._get_page_content(terms_path)

    @classmethod
    def get_policies(cls) -> str:
        """
        Return the Policies text file.
        """

        return cls._get_page_content(policies_path)

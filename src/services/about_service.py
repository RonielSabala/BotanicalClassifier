from pathlib import Path

from .i18n_service import i18n


class AboutService:
    @staticmethod
    def get_page_content(path: Path) -> str:
        str_path = str(path).format(lang=i18n.current_language)
        with open(str_path, "r", encoding="utf-8") as f:
            return f.read()

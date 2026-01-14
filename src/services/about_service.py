from .i18n_service import i18n


class AboutService:
    @staticmethod
    def get_page_content(path: str) -> str:
        path = path.format(lang=i18n.current_language)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

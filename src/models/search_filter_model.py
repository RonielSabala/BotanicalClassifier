from dataclasses import dataclass, field
from typing import Optional


@dataclass(slots=True)
class SearchFilter:
    search_text: Optional[str] = field(default=None)
    search_column: Optional[str] = field(default=None)

    def reset(self) -> None:
        self.search_text = None
        self.search_column = None

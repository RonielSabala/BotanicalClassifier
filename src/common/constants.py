"""
Application constants and defaults used by the GUI and image utilities.
"""

from dataclasses import dataclass
from datetime import date
from typing import Final

# GUI
WINDOW_WIDTH: Final[int] = 750
WINDOW_HEIGHT: Final[int] = 900

# Images
IMAGE_MODE: Final[str] = "RGBA"
IMAGE_BG_RGBA: Final[tuple[int, int, int, int]] = 0, 0, 0, 0
IMAGE_SIZE_PX: Final[int] = 128
IMAGE_FILENAME_PREFIX: Final[str] = "flower_survey"
ALLOWED_IMAGE_EXTENSIONS_STR: Final[str] = "*.png;*.jpg;*.jpeg"

# Copyright / Organization
COPYRIGHT_SYMBOL: Final[str] = "©"
CURRENT_YEAR: Final[int] = date.today().year
COMPANY_NAME: Final[str] = "Jardín Botánico Nacional"

# About / Contact
ABOUT_SUBTITLE: Final[str] = "Dr. Rafael M. Moscoso"
ABOUT_ADDRESS_INFO: Final[str] = (
    "Av. República de Colombia esq. Av. Los Próceres\n"
    "Sector los Altos de Galá, Santo Domingo, D.N."
)
ABOUT_PHONE_INFO: Final[str] = "(809) 385-2611 Ext. 221"
ABOUT_EMAIL_INFO: Final[str] = "jardinbotanico@jbn.gob.do"


@dataclass(slots=True, frozen=True)
class AboutInfo:
    subtitle: str
    address: str
    phone: str
    email: str


ABOUT: Final[AboutInfo] = AboutInfo(
    subtitle=ABOUT_SUBTITLE,
    address=ABOUT_ADDRESS_INFO,
    phone=ABOUT_PHONE_INFO,
    email=ABOUT_EMAIL_INFO,
)

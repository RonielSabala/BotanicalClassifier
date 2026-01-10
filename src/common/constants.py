# Window constants
WINDOW_NAME = "jbn"
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 900
MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080
WINDOW_PADX = int(MAX_WINDOW_WIDTH / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
WINDOW_PADY = int(MAX_WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT)
WINDOW_FOOTER = "Jardín Botánico Nacional\n©2025 Todos los derechos reservados."

_PROJECT_ROUTE = "src\\"

# Local storage
STORAGE_ROUTE = f"{_PROJECT_ROUTE}local_storage\\"
STORAGE_IMGS_ROUTE = f"{STORAGE_ROUTE}imgs"
STORAGE_RECORDS_ROUTE = f"{STORAGE_ROUTE}records.txt"

# Asset images
ASSET_IMGS_ROUTE = f"{_PROJECT_ROUTE}ui\\assets\\imgs\\"
ICON_IMG_ROUTE = f"{ASSET_IMGS_ROUTE}icon.png"
EMPTY_IMG_ROUTE = f"{ASSET_IMGS_ROUTE}empty.png"
BANNER_IMG_ROUTE = f"{ASSET_IMGS_ROUTE}banner.png"
SHIELD_IMG_ROUTE = f"{ASSET_IMGS_ROUTE}shield.png"

# Contact info
CONTACT_INFO_ROUTE = f"{_PROJECT_ROUTE}ui\\pages\\contact\\info\\"
FAQ_ROUTE = f"{CONTACT_INFO_ROUTE}/faq.txt"
TERMS_ROUTE = f"{CONTACT_INFO_ROUTE}/terms.txt"
POLICIES_ROUTE = f"{CONTACT_INFO_ROUTE}/policies.txt"

# Image constants
DEFAULT_IMG_SIZE = 128
DEFAULT_IMG_SELECT_STR = "<Selecciona una imagen>"

# - Table constants:

DEFAULT_TABLE_COLUMNS = (
    " ",
    "Subido por",
    "Apellido",
    "Ubicación",
    "Flor",
    "Predicción",
)

MAX_TABLE_ROW = 4
MAX_TABLE_COLUMN = len(DEFAULT_TABLE_COLUMNS)
FLOWER_COLUMN = DEFAULT_TABLE_COLUMNS.index("Flor")

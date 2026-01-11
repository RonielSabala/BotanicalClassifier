# Window constants
WINDOW_NAME = "jbn"
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 900
MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080
WINDOW_PADX = int(MAX_WINDOW_WIDTH / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
WINDOW_PADY = int(MAX_WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT)

# Page constants
PAGE_RETURN_BUTTON_TEXT = "Volver"
PAGE_FOOTER = "Jardín Botánico Nacional\n©2025 Todos los derechos reservados."

# Image constants
IMAGE_SIZE = 128
IMAGE_PREFIX = "flor_survey"
DEFAULT_IMAGE_ENTRY_TEXT = "<Selecciona una imagen>"

# Routes:

_PROJECT_ROUTE = "src\\"

# Local storage routes
_LOCAL_STORAGE_ROUTE = f"{_PROJECT_ROUTE}local_storage\\"
LOCAL_STORAGE_IMGS_ROUTE = f"{_LOCAL_STORAGE_ROUTE}images"
LOCAL_STORAGE_RECORDS_ROUTE = f"{_LOCAL_STORAGE_ROUTE}records.txt"

# Asset images routes
_IMAGES_ROUTE = f"{_PROJECT_ROUTE}ui\\assets\\images\\"
APP_ICON_IMAGE_ROUTE = f"{_IMAGES_ROUTE}app_icon.png"
APP_BANNER_IMAGE_ROUTE = f"{_IMAGES_ROUTE}app_banner.png"
COUNTRY_SHIELD_IMAGE_ROUTE = f"{_IMAGES_ROUTE}country_shield.png"
EMPTY_IMAGE_ROUTE = f"{_IMAGES_ROUTE}empty_image.png"

# About info routes
_ABOUT_INFO_ROUTE = f"{_PROJECT_ROUTE}ui\\pages\\about\\info\\"
FAQ_ROUTE = f"{_ABOUT_INFO_ROUTE}/faq.txt"
TERMS_ROUTE = f"{_ABOUT_INFO_ROUTE}/terms.txt"
POLICIES_ROUTE = f"{_ABOUT_INFO_ROUTE}/policies.txt"

# Window constants
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 900
MAX_WINDOW_WIDTH = 1920
MAX_WINDOW_HEIGHT = 1080
WINDOW_PADX = int(MAX_WINDOW_WIDTH / 2 + WINDOW_WIDTH / 2 - WINDOW_WIDTH)
WINDOW_PADY = int(MAX_WINDOW_HEIGHT / 2 + WINDOW_HEIGHT / 2 - WINDOW_HEIGHT)

# Images constants
IMAGE_SIZE = 128
IMAGE_MODE = "RGBA"
LOCAL_IMAGES_PREFIX = "flower_survey"
VALID_IMAGE_FILE_TYPES = "*.png;*.jpg;*.jpeg"

# Paths:

_PROJECT_DIR = "src\\"
I18N_DIR = f"{_PROJECT_DIR}i18n\\"

# Local storage paths
_LOCAL_STORAGE_DIR = f"{_PROJECT_DIR}local_storage\\"
LOCAL_STORAGE_IMGS_PATH = f"{_LOCAL_STORAGE_DIR}images"
LOCAL_STORAGE_RECORDS_PATH = f"{_LOCAL_STORAGE_DIR}records.txt"

# Asset images paths
_IMAGES_DIR = f"{_PROJECT_DIR}gui\\assets\\images\\"
APP_ICON_IMAGE_PATH = f"{_IMAGES_DIR}app_icon.png"
APP_BANNER_IMAGE_PATH = f"{_IMAGES_DIR}app_banner.png"
COUNTRY_SHIELD_IMAGE_PATH = f"{_IMAGES_DIR}country_shield.png"
EMPTY_IMAGE_PATH = f"{_IMAGES_DIR}empty_image.png"

# About info paths
_ABOUT_INFO_DIR = f"{_PROJECT_DIR}gui\\pages\\about\\info\\"
FAQ_PATH = f"{_ABOUT_INFO_DIR}faq.txt"
TERMS_PATH = f"{_ABOUT_INFO_DIR}terms.txt"
POLICIES_PATH = f"{_ABOUT_INFO_DIR}policies.txt"

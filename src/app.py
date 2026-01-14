from common.paths import (
    LOCAL_IMAGES_DIR,
    LOCAL_RECORDS_PATH,
    LOCAL_RESOURCES_DIR,
)
from gui import page
from gui.pages.menu_page import MenuPage

# Create local storage
LOCAL_RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_RECORDS_PATH.touch(exist_ok=True)

# Show menu page
MenuPage.show()
page.APP_ROOT.protocol("WM_DELETE_WINDOW", page.destroy_all_pages)
page.APP_ROOT.mainloop()

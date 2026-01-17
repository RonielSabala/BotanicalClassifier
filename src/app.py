from common.paths import (
    LOCAL_IMAGES_DIR,
    LOCAL_RECORDS_PATH,
    LOCAL_RESOURCES_DIR,
)
from gui import main as app
from gui.pages.menu_page import MenuPage

# Create local storage
LOCAL_RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_RECORDS_PATH.touch(exist_ok=True)

# Config app
app.set_window_title()

# Show menu page
MenuPage.show()
app.ROOT.mainloop()

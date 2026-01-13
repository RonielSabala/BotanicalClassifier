import os

from common.constants import (
    _LOCAL_DIR,
    LOCAL_IMGS_DIR,
    LOCAL_RECORDS_PATH,
)
from common.utils import is_valid_path
from gui import page
from gui.pages.menu_page import MenuPage

# Create local storage
if not is_valid_path(_LOCAL_DIR):
    os.mkdir(_LOCAL_DIR)
    os.mkdir(LOCAL_IMGS_DIR)
    with open(LOCAL_RECORDS_PATH, "w") as file:
        pass

# Show menu page
MenuPage.show()
page.TK_ROOT.protocol("WM_DELETE_WINDOW", page.destroy_all_pages)
page.TK_ROOT.mainloop()

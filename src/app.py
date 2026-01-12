import os

from common.constants import (
    _LOCAL_STORAGE_ROUTE,
    LOCAL_STORAGE_IMGS_ROUTE,
    LOCAL_STORAGE_RECORDS_ROUTE,
)
from common.utils import is_valid_route
from gui.pages import page
from gui.pages.menu_page import MenuPage

# Create local storage
if not is_valid_route(_LOCAL_STORAGE_ROUTE):
    os.mkdir(_LOCAL_STORAGE_ROUTE)
    os.mkdir(LOCAL_STORAGE_IMGS_ROUTE)
    with open(LOCAL_STORAGE_RECORDS_ROUTE, "w") as file:
        pass

# Show menu page
MenuPage.show()
page.TK_ROOT.protocol("WM_DELETE_WINDOW", page.destroy_all_pages)
page.TK_ROOT.mainloop()

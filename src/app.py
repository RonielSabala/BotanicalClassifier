import os

from common.constants import STORAGE_IMGS_ROUTE
from common.utils import is_valid_route
from ui.pages import page
from ui.pages.menu_page import MenuPage

# Create default image folder at local storage
if not is_valid_route(STORAGE_IMGS_ROUTE):
    os.mkdir(STORAGE_IMGS_ROUTE)

# Show menu page
MenuPage.show()
page.TK_ROOT.protocol("WM_DELETE_WINDOW", page.destroy_all_pages)
page.TK_ROOT.mainloop()

import os

from common.constants import STORAGE_IMGS_ROUTE
from ui.pages import page
from ui.pages.menu_page import Menu

# Create default image folder in the local storage
if not os.path.exists(STORAGE_IMGS_ROUTE):
    os.mkdir(STORAGE_IMGS_ROUTE)

# Start with menu page
Menu.show()
page.TK_ROOT.protocol("WM_DELETE_WINDOW", page.destroy_all_pages)
page.TK_ROOT.mainloop()

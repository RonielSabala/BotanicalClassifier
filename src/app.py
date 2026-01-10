import os

from common.constants import STORAGE_IMGS_ROUTE
from ui import main
from ui.pages.menu.main import Menu

# Crear carpeta donde se almacenarán las imágenes
if not os.path.exists(STORAGE_IMGS_ROUTE):
    os.mkdir(STORAGE_IMGS_ROUTE)

# Iniciar la ventana mostrando el menú
Menu.mostrar()

# Asociar la acción de cerrar la ventana con cerrar todas las páginas
main.TK_ROOT.protocol("WM_DELETE_WINDOW", main.close_pages)

# Bucle de la ventana
main.TK_ROOT.mainloop()

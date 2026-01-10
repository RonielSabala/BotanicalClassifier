import os

from common.constants import DATA_IMGS
from ui import main
from ui.pages.menu.main import Menu

# Crear carpeta donde se almacenarán las imágenes
if not os.path.exists(DATA_IMGS):
    os.mkdir(DATA_IMGS)

# Iniciar la ventana mostrando el menú
Menu.mostrar()

# Asociar la acción de cerrar la ventana con cerrar todas las páginas
main.RAIZ.protocol("WM_DELETE_WINDOW", main.close_pages)

# Bucle de la ventana
main.RAIZ.mainloop()

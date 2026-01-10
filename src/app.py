from UI import main
from UI.pages.menu.main import Menu

# Iniciar la ventana mostrando el menú
Menu.mostrar()

# Asociar la acción de cerrar la ventana con cerrar todas las páginas
main.RAIZ.protocol("WM_DELETE_WINDOW", main.close_pages)

# Bucle de la ventana
main.RAIZ.mainloop()

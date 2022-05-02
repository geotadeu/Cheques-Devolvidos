from tkinter import *
from exportador import *
from ui import *
from config import *

config = Config()
exportador = Exportador()
ui = UI(Tk())
ui.start(lambda: exportador.exportar(ui.rel_cb.get(), ui.get_coop(), ui.get_pa(), ui.path1, ui.path2, ui.path3))

#!/usr/bin/python3
"""
@author: MCruces

"""

from modules.gui_ascii import CellsAppASCII
from modules.cook_ascii import CookDataASCII
from utils.const import ASCII_DATA_DIR

# TODO:
#    - Barra de CMap a la derecha, para entender los colores
#    - Convertir a Hz los valores (creo que se va a quedar para cuando lea los hld)
#    y fijar los colores desde 0Hz hasta 2Hz (con valores superiores saturando)
#    - En lugar de tomar los archivos.dat, utilizar las cargas de los hld y
#    representarlos por cuartiles.
#    - Poder escoger fecha y hora para el rango de análisis.


if __name__ == "__main__":
    cook_data = CookDataASCII(data_dir=ASCII_DATA_DIR)
    CellsAppASCII(chef_object=cook_data)

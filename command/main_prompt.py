"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Author: Miguel Cruces Fernández
e-mail:
  - miguel.cruces.fernandez@usc.es
  - mcsquared.fz@gmail.com

Sources:
    https://code-maven.com/interactive-shell-with-cmd-in-python
    https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
"""
from cmd import Cmd


class Prompt(Cmd):
    def do_exit(self, inp):
        print(f"Bye {inp}!")
        return True

    @staticmethod
    def do_root(inp):
        from interface.gui_root import CellsAppROOT
        from kitchen.cook_root import CookDataROOT
        from utils.dirs import ROOT_DATA_DIR

        cook_data = CookDataROOT(data_dir=ROOT_DATA_DIR)
        # ary = cook_data.read_data()
        CellsAppROOT(chef_object=cook_data, theme="dark")

        # TODO:
        #  Extraer todos los archivos ascii y guardarlos en:
        #  Datos4TB/tragaldabas/data/monitoring/cellmaps
        #  con nombres más cortitos y útiles

    @staticmethod
    def do_ascii(inp):
        from interface.gui_ascii import CellsAppASCII
        from kitchen.cook_ascii import CookDataASCII
        from utils.dirs import ASCII_DATA_DIR

        # TODO:
        #    - Barra de CMap a la derecha, para entender los colores
        #    - Convertir a Hz los valores (creo que se va a quedar para cuando lea los hld)
        #    y fijar los colores desde 0Hz hasta 2Hz (con valores superiores saturando)
        #    - En lugar de tomar los archivos.dat, utilizar las cargas de los hld y
        #    representarlos por cuartiles.
        #    - Poder escoger fecha y hora para el rango de análisis.

        cook_data = CookDataASCII(data_dir=ASCII_DATA_DIR)
        CellsAppASCII(chef_object=cook_data)

    def do_add(self, inp):
        print(f"Adding \"{inp}\".")

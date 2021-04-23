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
    prompt = '(~ºuº)~ '
    intro = "\n"\
            "Welcome!\n"\
            "Type ? to list commands\n"

    theme = "dark"

    def do_exit(self, inp):
        print(f"Bye!")
        print()
        return True

    def help_exit(self):
        print("Write 'exit' to close this.")
        print()

    def do_root(self, inp):
        print("Launching ROOT reader User Graphical Interface...")

        from interface.gui_root import CellsAppROOT
        from kitchen.cook_root import CookDataROOT
        from utils.dirs import ROOT_DATA_DIR

        cook_data = CookDataROOT(data_dir=ROOT_DATA_DIR)
        # ary = cook_data.read_data()
        CellsAppROOT(chef_object=cook_data, theme=self.theme)

        # TODO:
        #  Extraer todos los archivos ascii y guardarlos en:
        #  Datos4TB/tragaldabas/data/monitoring/cellmaps
        #  con nombres más cortitos y útiles

        print("done")
        print()

    def help_root(self):
        print("Check utils/dirs.py and:")
        print("Add your path to root files in ROOT_DATA_DIR variable")
        print("Then run: root")
        print()

    def do_ascii(self, inp):
        print("Launching ASCII reader User Graphical Interface...")

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
        CellsAppASCII(chef_object=cook_data, theme=self.theme)

        print("done")
        print()

    def help_ascii(self):
        print("Check utils/dirs.py and:")
        print("Add your path to root files in ASCII_DATA_DIR variable")
        print("Then run: ascii")
        print()

    def do_theme(self, theme):
        if theme not in ["dark", "light"]:
            print("Only dark and light themes available.")
        self.theme = theme
        print(f"--> \"{theme}\" theme set.")
        print()

    def help_theme(self):
        print("Usage:")
        print("theme dark: Use dark theme")
        print("theme light: Use light theme")
        print("Changes will be lost when you close this prompt")
        print()

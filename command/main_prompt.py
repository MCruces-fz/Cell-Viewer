"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Author: Miguel Cruces Fernández
e-mail:
  - miguel.cruces.fernandez@usc.es
  - mcsquared.fz@gmail.com
"""
from cmd import Cmd


class Prompt(Cmd):
    prompt = '(~ºuº)~ '
    intro = "\n"\
            "Welcome!\n"\
            "Type ? to list commands\n"

    theme = "dark"

    @staticmethod
    def do_exit(inp):
        print(f"Bye!")
        print()
        return True

    def default(self, inp):
        if inp in ["x", "q", ".q", ":q"]:
            return self.do_exit(inp)
        else:
            print(f"Unknown syntax: {inp}")

    @staticmethod
    def help_exit():
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

        print("done")
        print()

    @staticmethod
    def help_root():
        print("Check utils/dirs.py and:")
        print("Add your path to root files in ROOT_DATA_DIR variable")
        print("Then run: root")
        print()

    def do_ascii(self, inp):
        print("Launching ASCII reader User Graphical Interface...")

        from interface.gui_ascii import CellsAppASCII
        from kitchen.cook_ascii import CookDataASCII
        from utils.dirs import ASCII_DATA_DIR

        cook_data = CookDataASCII(data_dir=ASCII_DATA_DIR)
        CellsAppASCII(chef_object=cook_data, theme=self.theme)

        print("done")
        print()

    @staticmethod
    def help_ascii():
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

    @staticmethod
    def help_theme():
        print("Usage:")
        print("theme dark: Use dark theme")
        print("theme light: Use light theme")
        print("Changes will be lost when you close this prompt")
        print()

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
import json
import os


class Prompt(Cmd):
    prompt = '(~ºuº)~ '
    intro = ("\n"
             "      ____     _ _    __     ___                        \n"
             "     / ___|___| | |   \ \   / (_) _____      _____ _ __ \n"
             "    | |   / _ \ | |____\ \ / /| |/ _ \ \ /\ / / _ \ '__|\n"
             "    | |__|  __/ | |_____\ V / | |  __/\ V  V /  __/ |   \n"
             "     \____\___|_|_|      \_/  |_|\___| \_/\_/ \___|_|   \n"
             "    \n\n"
             "       Cell-Viewer is open and freely distributable\n"
             "       https://github.com/MCruces-fz/Cell-Viewer.git\n"
             "    \n\n"
             "    type   ? / help                    if you are new!\n"
             "    type   help <command>              for help with any <command>\n"
             "    type   :q / .q / q / x / exit      to exit\n")

    def __init__(self):
        super().__init__()
        self.config = self.load_config()

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
        print(f"Launching ROOT reader User Graphical Interface... {inp}")

        from interface.gui_root import CellsAppROOT
        from kitchen.cook_root import CookDataROOT
        from utils.dirs import ROOT_DATA_DIR

        cook_data = CookDataROOT(data_dir=ROOT_DATA_DIR)
        # ary = cook_data.read_data()
        CellsAppROOT(chef_object=cook_data, theme=self.config["theme"])

        print("done")
        print()

    @staticmethod
    def help_root():
        print("This command launches the Graphical User Interface for checking")
        print("the state of the Tragaldabas detector.")
        print("For more information, check the README:")
        print("https://github.com/MCruces-fz/Cell-Viewer/blob/master/README.md")
        print()

    def do_ascii(self, inp):
        print(f"Launching ASCII reader User Graphical Interface... {inp}")

        from interface.gui_ascii import CellsAppASCII
        from kitchen.cook_ascii import CookDataASCII
        from utils.dirs import ASCII_DATA_DIR

        cook_data = CookDataASCII(data_dir=ASCII_DATA_DIR)
        CellsAppASCII(chef_object=cook_data, theme=self.config["theme"])

        print("done")
        print()

    @staticmethod
    def help_ascii():
        print("This command launches the Graphical User Interface for checking")
        print("the state of the Tragaldabas detector.")
        print("For more information, check the README:")
        print("https://github.com/MCruces-fz/Cell-Viewer/blob/master/README.md")
        print()

    def do_theme(self, theme):
        if theme not in ["dark", "light"]:
            print("Only dark and light themes available.")
            print()
        else:
            self.config["theme"] = theme
            self.save_config()
            print(f"--> \"{theme}\" theme set.")
            print()

    def help_theme(self):
        print(f"Current theme: {self.config['theme']}")
        print()
        print("Usage:")
        print("theme dark: Use dark theme")
        print("theme light: Use light theme")
        print()

    def do_settings(self, inp):
        print(f"Current settings:  {inp}")
        print(json.dumps(self.config, indent=4))
        print()

    @staticmethod
    def help_settings():
        print("Shows the current settings.")

    def save_config(self):
        with open("command/settings.json", "w+") as settings:
            json.dump(self.config, settings, indent=4)

    @staticmethod
    def load_config():
        if not os.path.isfile("command/settings.json"):
            configuration = {
                "theme": "dark"
            }
            with open("command/settings.json", "w+") as settings:
                json.dump(configuration, settings)

        with open("command/settings.json", "r+") as settings:
            config = json.load(settings)

        return config

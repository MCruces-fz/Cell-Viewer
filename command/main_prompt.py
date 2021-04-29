"""
             A P A C H E   L I C E N S E
                    ------------ 
              Version 2.0, January 2004

       Copyright 2021 Miguel Cruces Fernández

  Licensed under the Apache License, Version 2.0 (the 
"License"); you may not use this file except in compliance 
with the License. You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, 
software distributed under the License is distributed on an 
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
either express or implied. See the License for the specific 
language governing permissions and limitations under the 
License.

           miguel.cruces.fernandez@usc.es
               mcsquared.fz@gmail.com

"""
from cmd import Cmd
import json
import os
import datetime


class Prompt(Cmd):
    prompt = '(~ºuº)~ '
    intro = ("\n"
             "             ____     _ _    __     ___                        \n"
             "            / ___|___| | |   \ \   / (_) _____      _____ _ __ \n"
             "           | |   / _ \ | |____\ \ / /| |/ _ \ \ /\ / / _ \ '__|\n"
             "           | |__|  __/ | |_____\ V / | |  __/\ V  V /  __/ |   \n"
             "            \____\___|_|_|      \_/  |_|\___| \_/\_/ \___|_|   \n"
             "           \n\n"
             "              Cell-Viewer is open and freely distributable\n"
             "              https://github.com/MCruces-fz/Cell-Viewer.git\n"
             "    \n\n"
             "    type   ? / help                    if you are new!\n"
             "    type   root                        to launch the GUI for ROOT  files.\n"
             "    type   ascii                       to launch the GUI for ASCII files.\n"
             "    type   source                      to check source directories.\n"
             "    type   theme dark / light          to switch between dark and light theme.\n"
             "    type   help <command>              for help with any <command>.\n"
             "    type   :q / .q / q / x / exit      to exit.\n")

    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.setup()

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

    @staticmethod
    def do_source(inp):
        from utils.dirs import ASCII_DATA_DIR, ROOT_DATA_DIR, TRUFA_LIB_DIR
        print("Source Directories:")
        print(f"ASCII_DATA_DIR: {ASCII_DATA_DIR}")
        print(f"ROOT_DATA_DIR:  {ROOT_DATA_DIR}")
        print(f"TRUFA_LIB_DIR:  {TRUFA_LIB_DIR}")
        print()
        print("Type 'source root / ascii' to check files inside.")
        print()
        print("(Edit utils/dirs.py to change them)")
        print()

        if inp == "root":
            directory = ROOT_DATA_DIR
        elif inp == "ascii":
            directory = ASCII_DATA_DIR
        elif inp in ["", " "]:
            return 0
        else:
            print(f"There isn't any directory called {inp}")
            return 0

        print()
        print(f"Files in {directory}:")
        for file in sorted(os.listdir(directory)):
            print(file)

    @staticmethod
    def help_source():
        print("It shows source directories.")
        print()
        print("To check files in root / ascii directory, type:")
        print("source root / ascii")
        print()

    @staticmethod
    def do_doy(inp):
        try:
            year, doy = inp.split("/")
        except ValueError:
            print("Input must be YY/DOY or YYYY/DOY")
            return 0

        if len(year) == 4:
            year = int(year)
        elif len(year) == 2:
            year = int(f"20{year}")
        else:
            print("Year must be like '2021' or like '21'")
            return 0
        doy = int(doy)

        output = datetime.date(year=year, month=1, day=1) + datetime.timedelta(days=doy - 1)
        print("yyyy-mm-dd")
        print(output)
        print()

    @staticmethod
    def do_date(inp):
        try:
            year, month, day = inp.split("/")
        except ValueError:
            print("Input must be YY/MM/DD or YYYY/MM/DD")
            return 0

        if len(year) == 4:
            year = int(year)
        elif len(year) == 2:
            year = int(f"20{year}")
        else:
            print("Year must be like '2021' or like '21'")
            return 0
        
        month = int(month)
        day = int(day)

        try:
            output = datetime.date(year=year, month=month, day=day).strftime("%Y-%j")
        except Exception as e:
            print(e.__doc__)
            print(e)
            return 0

        print("yyyy-doy")
        print(output)
        print()

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

    @staticmethod
    def setup():
        if not os.path.isfile("utils/dirs.py"):
            directories = (
                'ASCII_DATA_DIR = "/path/to/png/"'
                'ROOT_DATA_DIR  = "/path/to/rootfiles/"'
                'TRUFA_LIB_DIR  = "/path/to/libtunpacker.so"'
            )
            with open("utils/dirs.py", "w+") as dirs:
                dirs.write(directories)

            print("WARNING!!")
            print("Go to utils/dirs.py and edit the variables as is")
            print("documented in README.md")
            print("https://github.com/MCruces-fz/Cell-Viewer/blob/master/README.md")
            print("")


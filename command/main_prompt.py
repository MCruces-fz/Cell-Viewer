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
             "    type   help <command>              to get information about <command>.\n"
             "    type   root                        to launch the GUI for ROOT  files.\n"
             "    type   ascii                       to launch the GUI for ASCII files.\n"
             "    type   source                      to check  or edit source directories.\n"
             "    type   doy YY/DOY                  to calculate date in format yyyy-mm-dd.\n"
             "    type   date YY/MM/DD               to calculate date in format yyyy-doy.\n"
             "    type   theme dark / light          to switch between dark and light theme.\n"
             "    type   help <command>              for help with any <command>.\n"
             "    type   :q / .q / q / x / exit      to exit and save settings.\n")

    root_data_dir = None
    ascii_data_dir = None
    trufa_lib_dir = None

    def __init__(self):
        super().__init__()
        self.setup()
        self.config = self.load_config()

    def do_exit(self, inp):
        print(f"Bye!")
        print()
        self.save_config()
        return True

    def default(self, inp):
        if inp in ["x", "q", ".q", ":q"]:
            return self.do_exit(inp)
        else:
            print(f"Unknown syntax: {inp}")

    def do_EOF(self, line):
        return self.do_exit(line)

    @staticmethod
    def help_exit():
        print("Write 'exit' to close this.")
        print()

    def do_root(self, inp):
        print(f"Launching ROOT reader User Graphical Interface... {inp}")

        from interface.gui_root import CellsAppROOT
        from kitchen.cook_root import CookDataROOT

        cook_data = CookDataROOT(data_dir=self.root_data_dir)
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

        cook_data = CookDataASCII(data_dir=self.ascii_data_dir)
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
        print("Saved in command/settings.json")
        print()

    @staticmethod
    def help_settings():
        print("Shows the current settings.")

    def do_source(self, inp):
        args = inp.split(" ")

        def show(cls):
            print("Source Directories:")
            print(f"ROOT data:  {cls.root_data_dir}")
            print(f"ASCII data: {cls.ascii_data_dir}")
            print(f"TRUFA library:  {cls.trufa_lib_dir}")
            print()

        if args[0] in ["show"]:
            show(self)
            if len(args) == 2:
                if args[1] == "root":
                    directory = self.root_data_dir
                elif args[1] == "ascii":
                    directory = self.ascii_data_dir
                elif args[1] in ["", " "]:
                    print("   -   ")
                    return 0
                else:
                    print(f"There isn't any directory called {inp}")
                    return 0

                print(f"Files in {directory}:")
                for file in sorted(os.listdir(directory)):
                    print(file)
                print()
        elif args[0] == "edit":
            if len(args) != 3:
                print("Usage:")
                print("    source edit <dir> <slot-name>")
                print("Example:")
                print("    source edit root main")
                return 0

            print("Type or paste directory:")
            inp_dir = input()
            if not os.path.isdir(inp_dir):
                print(f"Directory doesn't exist: {inp_dir}")
            else:
                self.config["dirs"][args[1]][args[2]] = inp_dir

            self.save_config()
        elif args[0] == "set":
            if len(args) != 3:
                print("Usage:")
                print("    source set <dir> <slot-name>")
                print("Example:")
                print("    source set root data")
                return 0

            if args[1] == "root":
                if args[2] not in self.config["dirs"]["root"].keys():
                    print(f"There isn't '{args[2]}' option in root sources.")
                    print("You can choose:")
                    for key in self.config["dirs"]["root"]:
                        print(f"  - {key}: {self.config['dirs']['root'][key]}")
                    return 0
                self.config["dirs"]["root"]["main"] = self.config["dirs"]["root"][args[2]]
                self.root_data_dir = self.config["dirs"]["root"]["main"]
            elif args[1] == "ascii":
                if args[2] not in self.config["dirs"]["ascii"].keys():
                    print(f"There isn't '{args[2]}' option in ascii sources.")
                    print("You can choose:")
                    for key in self.config["dirs"]["ascii"]:
                        print(f"  - {key}: {self.config['dirs']['ascii'][key]}")
                    return 0
                self.config["dirs"]["ascii"]["main"] = self.config["dirs"]["ascii"][args[2]]
                self.ascii_data_dir = self.config["dirs"][args[1]][args[2]]
            else:
                print(f"Bad option: '{args[1]}'. It must be 'ascii' or 'root'")
                return 0

            self.save_config()
        else:
            show(self)
            print("Type 'help source' to see all features.")
            print()
            return 0

    @staticmethod
    def help_source():
        print("Usage:")
        print("    source                             basic view")
        print("    source show                        to show source directories")
        print("    source show <dir>                  to check files in root / ascii directories")
        print("    source edit <dir> <slot-name>      to add / edit another directory")
        print("    source set <dir> <slot-name>       to set as default an existent directory")
        print()
        print("with <dir> in (ascii, root)")
        print("with <slot-name> any string")
        print("    to check all <slot-name>s, type settings.")
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

    def help_doy(self):
        print("Command to calculate date in format yyyy-mm-dd from day of the year")
        print("format: yy-doy or yyyy-doy")
        print()
        print("Usage:")
        print(f"{self.prompt}doy YY/DOY")
        print("or")
        print(f"{self.prompt}doy YYYY/DOY")
        print()
        print("For instance:")
        print(f"{self.prompt}doy 21/123")
        print("yyyy-mm-dd")
        print("2021-05-03")
        print("or")
        print(f"{self.prompt}doy 2021/321")
        print("yyyy-mm-dd")
        print("2021-11-17")
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

    def help_date(self):
        print("Command to calculate date in format yyyy-doy from date in ")
        print("format: yy-mm-dd or yyyy-mm-dd")
        print()
        print("Usage:")
        print(f"{self.prompt}date YY/MM/DD")
        print("or")
        print(f"{self.prompt}date YYYY/MM/DD")
        print()
        print("For instance:")
        print(f"{self.prompt}date 21/05/03")
        print("yyyy-doy")
        print("2021-123")
        print("or")
        print(f"{self.prompt}date 2021/11/17")
        print("yyyy-doy")
        print("2021-321")
        print()

    def save_config(self):
        with open("command/settings.json", "w+") as settings:
            json.dump(self.config, settings, indent=4)

    def load_config(self):
        if not os.path.isfile("command/settings.json"):
            try:
                from utils.dirs import ROOT_DATA_DIR, ASCII_DATA_DIR, TRUFA_LIB_DIR
                main_root_dir = ROOT_DATA_DIR
                main_ascii_dir = ASCII_DATA_DIR
                trufa_lib_dir = TRUFA_LIB_DIR
            except Exception as e:
                print(e)
                print(e.__doc__)
                e_name = e.__class__.__name__
                if e_name == "ModuleNotFoundError":
                    print("You need to edit main directories manually "
                          "in command/settings.json")
                elif e_name == "ImportError":
                    print("You need to edit main directories manually "
                          "in command/settings.json")
                else:
                    print("Bad option")
                main_root_dir = "/path/to/rootfiles/"
                main_ascii_dir = "/path/to/png/"
                trufa_lib_dir = "/path/to/trufa_dir/"

            configuration = {
                "theme": "dark",
                "dirs": {
                    "root": {
                        "main": main_root_dir
                    },
                    "ascii": {
                        "main": main_ascii_dir
                    },
                    "trufa": trufa_lib_dir
                }
            }
            with open("command/settings.json", "w+") as settings:
                json.dump(configuration, settings, indent=4)

        with open("command/settings.json", "r+") as settings:
            config = json.load(settings)

        self.root_data_dir = config["dirs"]["root"]["main"]
        self.ascii_data_dir = config["dirs"]["ascii"]["main"]
        self.trufa_lib_dir = config["dirs"]["trufa"]

        return config

    @staticmethod
    def setup():
        if not os.path.isfile("utils/dirs.py"):
            directories = (
                'ASCII_DATA_DIR = "/path/to/png/"'
                'ROOT_DATA_DIR  = "/path/to/rootfiles/"'
                'TRUFA_LIB_DIR  = "/path/to/TRUFA/"'
            )
            with open("utils/dirs.py", "w+") as dirs:
                dirs.write(directories)

            print("WARNING!!")
            print("Go to utils/dirs.py and edit the variables as is")
            print("documented in README.md")
            print("https://github.com/MCruces-fz/Cell-Viewer/blob/master/README.md")
            print("")

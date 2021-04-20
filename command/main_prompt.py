"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Sources:
    https://code-maven.com/interactive-shell-with-cmd-in-python
    https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
"""
from cmd import Cmd


class Prompt(Cmd):
    def do_exit(self, inp):
        print(f"Bye {inp}!")
        return True

    def do_add(self, inp):
        print(f"Adding \"{inp}\".")

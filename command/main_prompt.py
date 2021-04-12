from cmd import Cmd


class Prompt(Cmd):
    def do_exit(self, inp):
        print(f"Bye {inp}!")
        return True

    def do_add(self, inp):
        print(f"Adding \"{inp}\".")

try:  # Python 3
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # Python 2.7
    import Tkinter as tk
    import ttk

import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    from tkcalendar import DateEntry, Calendar
except ModuleNotFoundError:
    install("tkcalendar")
    from tkcalendar import DateEntry, Calendar

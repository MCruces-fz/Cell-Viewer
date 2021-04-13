from interface.parent_gui import CellsApp
from kitchen.cook_root import CookDataROOT
from kitchen.chef import Chef
from utils.tkinter_modules import tk
from utils.const import NCOL, NROW

import numpy as np
import datetime
from typing import Union


class CellsAppROOT(CellsApp):
    def __init__(self, chef_object: Union[Chef, CookDataROOT], window_title=None, theme: str = "dark"):
        self.chk_m1 = None
        super().__init__(chef_object, window_title, theme)
        self.var_hour_from = None
        self.var_mins_from = None
        self.var_hour_to = None
        self.var_mins_to = None

    def set_spinbox(self, master: object, var: object, f: int = 0, t: int = 1):
        """
        Custom Spinbox for set time HH:MM.

        :param master: Parent frame
        :param var: Variable to set the chosen value
        :param f: value to start from (default 0)
        :param t: value to end spinbox (default 1)
        :return: Spinbox object
        """
        spx = tk.Spinbox(master, from_=f, to=t, width=2,
                         wrap=True, textvariable=var,
                         bg=self.bg_default, fg=self.fg_default,
                         buttonbackground=self.bg_default, bd=0)
        return spx

    def choose_options(self):
        """
        L A Y O U T

        This updated the frame where the buttons to choose options are placed.
        """

        super().choose_options()

        # Choose time
        lbl_time = tk.Label(master=self.frm_datime, text='HH:MM (24h)',
                            bg=self.bg_default, fg=self.fg_default)

        self.var_hour_from = tk.IntVar(value=0)
        self.var_mins_from = tk.IntVar(value=0)
        self.var_hour_to = tk.IntVar(value=0)
        self.var_mins_to = tk.IntVar(value=0)

        spx_hour_from = self.set_spinbox(self.frm_datime, self.var_hour_from, t=23)
        spx_mins_from = self.set_spinbox(self.frm_datime, self.var_mins_from, t=59)
        spx_hour_to = self.set_spinbox(self.frm_datime, self.var_hour_to, t=23)
        spx_mins_to = self.set_spinbox(self.frm_datime, self.var_mins_to, t=59)

        lbl_time.grid(row=0, column=2, columnspan=2)
        spx_hour_from.grid(row=1, column=2)
        spx_mins_from.grid(row=1, column=3)
        spx_hour_to.grid(row=2, column=2)
        spx_mins_to.grid(row=2, column=3)

        self.chk_m1 = tk.BooleanVar(master=self.frm_choices)

        chk_multi = tk.Checkbutton(self.frm_choices, text="M1 only", variable=self.chk_m1,
                                   bg=self.bg_default, fg=self.fg_default, selectcolor=self.bg_default)
        chk_multi.grid(row=5, column=2)

    def show_mambos(self):

        # Destroy MMBOS frame if it exists
        try: self.frm_mmbos.destroy()
        except AttributeError: pass

        # Show MMBOS
        self.frm_mmbos = tk.Frame(master=self.frm_options, bg=self.bg_default)

        sum_mb1 = self.mambo_sum('MB1')
        btn_mb1 = tk.Button(
            self.frm_mmbos,
            text=f"{sum_mb1}",
            command=lambda n="MB1": print(n),
            bg=self.bg_default,
            fg=self.fg_default,
            bd=0
        )
        sum_mb2 = self.mambo_sum('MB2')
        btn_mb2 = tk.Button(
            self.frm_mmbos,
            text=f"{sum_mb2}",
            command=lambda n="MB2": print(n),
            bg=self.bg_default,
            fg=self.fg_default,
            bd=0
        )
        sum_mb3 = self.mambo_sum('MB3')
        btn_mb3 = tk.Button(
            self.frm_mmbos,
            text=f"{sum_mb3}",
            command=lambda n="MB3": print(n),
            bg=self.bg_default,
            fg=self.fg_default,
            bd=0
        )
        sum_mb4 = self.mambo_sum('MB4')
        btn_mb4 = tk.Button(
            self.frm_mmbos,
            text=f"{sum_mb4}",
            command=lambda n="MB4": print(n),
            bg=self.bg_default,
            fg=self.fg_default,
            bd=0
        )
        sum_all = self.mambo_sum("ALL")
        btn_all = tk.Button(
            self.frm_mmbos,
            text=f"{sum_all}",
            command=lambda n="All MBs": print(n),
            bg=self.bg_default,
            fg=self.fg_default,
            bd=0
        )

        self.frm_mmbos.grid(row=1, column=4)
        btn_mb1.grid(row=2, column=2, sticky="news")
        btn_mb2.grid(row=1, column=2, sticky="news")
        btn_mb3.grid(row=1, column=1, sticky="news")
        btn_mb4.grid(row=2, column=1, sticky="news")
        btn_all.grid(row=3, column=1, columnspan=2, sticky="news")

    def mambo_sum(self, mambo: Union[str, int]):
        """
        Get sum of values


        """
        numpy_data = self.get_math_value(val=self.choice_math_val.get())

        if type(numpy_data) not in [np.ndarray, np.array]:
            return 0

        if mambo in ["MB1", "mb1", 1]:
            total = np.sum(numpy_data[NROW // 2:, NCOL // 2:])
        elif mambo in ["MB2", "mb2", 2]:
            total = np.sum(numpy_data[:NROW // 2, NCOL // 2:])
        elif mambo in ["MB3", "mb3", 3]:
            total = np.sum(numpy_data[:NROW // 2, :NCOL // 2])
        elif mambo in ["MB4", "mb4", 4]:
            total = np.sum(numpy_data[NROW // 2:, :NCOL // 2])
        elif mambo in ["ALL", "all", "All", 0]:
            total = np.sum(numpy_data)
        else:
            raise Exception("Wrong value of mambo.")

        return total

    def grid_button(self, master: object, i: int, j: int, bg_color: str = "#000000", fg_color: str = "#ffffff"):
        """
        Tkinter Button object, prepared for stack on the grid.

        :param master: Parent frame
        :param i: Index of the row
        :param j: Index of the column
        :param bg_color: (optional) background color
        :param fg_color: (optional) foreground color.
        :return: tk.Button object
        """
        value_name = self.choice_math_val.get()
        if value_name == "hits rate":
            txt = f"{self.get_math_value(val=value_name)[i, j]:.1f} Hz"
        elif value_name == "reco. rate":
            txt = f"{self.get_math_value(val=value_name)[i, j]:.3f}"
        elif value_name in ["reco. hits", "raw hits"]:
            txt = f"{self.get_math_value(val=value_name)[i, j]:.0f}"
        else:
            raise Exception(f"Problem in grid_button method with chosen variable name, {value_name} is"
                            f"not in [hits rate, reco. rate, reco. hits, raw hits]")

        button_obj = tk.Button(master=master,
                               text=txt,
                               height=2, width=4,
                               bg=bg_color, fg=fg_color,
                               command=lambda a=i, b=j: self.cell_button(a, b), bd=0)
        return button_obj

    def cell_button(self, row_id: int, col_id: int):
        """
        Create the function for each button. Only passed to override parent method.

        :param row_id: Row ID of the cell
        :param col_id: Column ID of the cell
        """
        pass

    def get_math_value(self, val: str) -> np.array:
        """
        Function which returns the array corresponding to the given string.

        :param val: String with the name of the desired array ("raw hits", "hits rate", "reco. hits").
        :return: Array with the shape of the detector plane.
        """
        if self.from_date is None or self.to_date is None:
            return 0
        if val == "raw hits":
            return self.inp_dt.raw_hits
        elif val == "hits rate":
            return self.inp_dt.raw_hits_hz
        elif val == "reco. hits":
            return self.inp_dt.saetas
        elif val == "reco. rate":
            return self.inp_dt.saetas_hz
        else:
            raise Exception("Failed val in get_math_value()")

    def update_datetime(self):
        """
        Update the date and time global variables
        """
        self.from_date = datetime.datetime.combine(
            self.cal_from.get_date(),
            datetime.time(hour=self.var_hour_from.get(), minute=self.var_mins_from.get())
        )
        self.to_date = datetime.datetime.combine(
            self.cal_to.get_date(),
            datetime.time(hour=self.var_hour_to.get(), minute=self.var_mins_to.get())
        )

    def refresh(self):
        self.inp_dt.check_m1 = self.chk_m1.get()

        super().refresh()

        self.show_mambos()

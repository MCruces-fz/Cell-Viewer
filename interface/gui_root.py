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

from interface.parent_gui import CellsApp
from kitchen.cook_root import CookDataROOT
from kitchen.chef import Chef
from figmap.cellmap import Cellmap
from utils.tkinter_modules import tk
from utils.const import NCOL, NROW

import numpy as np
import datetime
# import matplotlib.pyplot as plt
from typing import Union
# from os.path import join as join_path


class CellsAppROOT(CellsApp):
    def __init__(self, chef_object: Union[Chef, CookDataROOT], window_title=None, theme: str = "dark"):
        self.chk_m1 = None
        self.chk_hz = None
        super().__init__(chef_object, window_title, theme)
        self.var_hour_from = None
        self.var_mins_from = None
        self.var_hour_to = None
        self.var_mins_to = None
        self.var_max_color = None

        self.cell_map = None

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

        # CHOOSE TIME
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

        # CHECKS
        # Max value to color
        self.chk_max = tk.BooleanVar(master=self.frm_choices)
        chk_mx = tk.Checkbutton(self.frm_choices, text="Max: ", variable=self.chk_max,
                                bg=self.bg_default, fg=self.fg_default, selectcolor=self.bg_default)
        self.var_max_color = tk.StringVar(master=self.frm_choices, value="0.8")
        ent_max = tk.Entry(master=self.frm_choices, textvariable=self.var_max_color,
                           bg=self.bg_default, fg=self.fg_default, width=7)
        chk_mx.grid(row=4, column=1)
        ent_max.grid(row=4, column=2)

        # Other checks
        self.chk_m1 = tk.BooleanVar(master=self.frm_choices)
        chk_multi = tk.Checkbutton(self.frm_choices, text="M1 only", variable=self.chk_m1,
                                   bg=self.bg_default, fg=self.fg_default, selectcolor=self.bg_default)
        chk_multi.grid(row=4, column=3)

        self.chk_hz = tk.BooleanVar(master=self.frm_choices)
        chk_hertz = tk.Checkbutton(self.frm_choices, text="Rate (Hz)", variable=self.chk_hz,
                                   bg=self.bg_default, fg=self.fg_default, selectcolor=self.bg_default)
        chk_hertz.grid(row=5, column=3)

        # SAVE BUTTON
        btn_save = tk.Button(
            master=self.window, text="SAVE",
            command=self.save_state_png,
            bg=self.bg_default, fg=self.fg_default,
            bd=0
        )
        btn_save.pack()

    def save_state_png(self):

        self.cellmap.update(
            cooked=self.inp_dt,
            hz=self.chk_hz.get()
        )
        self.cellmap.set_mapper(
            set_max=self.chk_max.get(),
            max_val=self.var_max_color.get(),
            cmap_name=self.choice_cmap.get()
        )

        self.cellmap.save_file(ext="png")

    def show_mambos(self):

        try:
            self.frm_mmbos.destroy()
        except AttributeError:
            pass

        self.frm_mmbos = tk.Frame(master=self.frm_options, bg=self.bg_default)

        if self.chk_hz.get():
            significant = 3
        else:
            significant = 1

        sum_mbos = np.array([
            [self.mambo_sum('MB3'), self.mambo_sum('MB2')],
            [self.mambo_sum('MB4'), self.mambo_sum('MB1')]
        ])
        mean_mbos = np.round(sum_mbos / 30, significant)

        for r, row in enumerate(sum_mbos):
            for c, sum_val in enumerate(row):
                mean_val = mean_mbos[r, c]
                bg_color, fg_color = self.cellmap.set_value_color(mean_val)
                btn_mb = tk.Button(
                    self.frm_mmbos,
                    text=f"{mean_val}",
                    command=lambda s=sum_val, m=mean_val: print(f"\nSum: {s}\nMean: {m:.3f}"),
                    bg=bg_color,
                    fg=fg_color,
                    bd=0
                )
                btn_mb.grid(row=r + 1, column=c + 1, sticky="news")

        sum_all = self.mambo_sum("ALL")
        mean_all = np.round(sum_all / 120, significant)
        bg_color, fg_color = self.cellmap.set_value_color(mean_all)
        btn_all = tk.Button(
            self.frm_mmbos,
            text=f"{mean_all}",
            command=lambda s=sum_all, m=mean_all: print(f"Sum: {s}\nMean: {m:.3f}"),
            bg=bg_color,
            fg=fg_color,
            bd=0
        )

        btn_all.grid(row=3, column=1, columnspan=2, sticky="news")
        self.frm_mmbos.grid(row=1, column=4)

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
        value = self.get_math_value(self.choice_math_val.get())[i, j]
        if self.chk_hz.get():
            txt = f"{value:.3f}"
        else:
            txt = f"{value:.0f}"

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
        return self.inp_dt.plane_event

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
        self.inp_dt.check_hz = self.chk_hz.get()

        super().refresh()

        self.show_mambos()

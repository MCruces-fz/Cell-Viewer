"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
"""

from interface.parent_gui import CellsApp
from kitchen.cook_ascii import CookDataASCII
from kitchen.chef import Chef
from utils.tkinter_modules import tk

import matplotlib.pyplot as plt
import numpy as np
from typing import Union


class CellsAppASCII(CellsApp):
    def __init__(self, chef_object: Union[Chef, CookDataASCII], window_title=None, theme: str = "dark"):
        """
        Constructor of the GUI

        :param chef_object: Object to get data. It has to have the following:
            - METHOD:
                * update(from_date, to_date, plane_name)
            - ATTRIBUTES:
                * all_data
                * mean
                * std
                * skewness
                * kurtosis
        :param window_title: (optional) String with the title of the window
        :param theme: (optional) dark or light (default dark).
        """
        super().__init__(chef_object, window_title, theme)

    def update_datetime(self):
        self.from_date = self.cal_from.get_date()
        self.to_date = self.cal_from.get_date()

    def grid_button(self, master, i, j, bg_color="#000000", fg_color="#ffffff"):
        """
        Tkinter Button object, prepared for stack on the grid.

        :param master: Parent frame
        :param i: Index of the row
        :param j: Index of the column
        :param bg_color: (optional) background color
        :param fg_color: (optional) foreground color.
        :return: tk.Button object
        """
        button_obj = tk.Button(master=master,
                               text=f"{self.get_math_value(val=self.choice_math_val.get())[i, j]:.0f}",
                               height=2, width=4,
                               bg=bg_color, fg=fg_color,
                               command=lambda a=i, b=j: self.cell_button(a, b), bd=0)
        return button_obj

    def cell_button(self, row_id, col_id):
        """
        Create the function for each button. It displays
        a matplotlib graph

        :param row_id: Row ID of the cell
        :param col_id: Column ID of the cell
        """

        all_hits = self.inp_dt.all_data[:, row_id, col_id]
        mean = self.inp_dt.mean[row_id, col_id]
        std = self.inp_dt.std[row_id, col_id]

        plt.figure(f"cell ({row_id}, {col_id})")
        plt.title(f"Plane {self.plane_name} - Cell index ({row_id}, {col_id})")

        plt.hist(all_hits, color='c', edgecolor='k', alpha=0.65)
        plt.axvline(mean, color='k', linestyle='dashed', linewidth=1, label=f'Mean: {mean:.2f}')
        min_ylim, max_ylim = plt.ylim()
        plt.errorbar(x=mean, y=max_ylim * 0.68, xerr=std, color='k', label=f'Std.: {std:.2f}')
        plt.yscale("log")

        plt.xlabel("Number of hits")
        plt.ylabel("Counts")
        plt.legend(loc="best")

        plt.show()

    def get_math_value(self, val: str) -> np.array:
        """
        Function which returns the array corresponding to the given string.

        :param val: String with the name of the desired array (mean, sigma, skewness, kurtosis).
        :return: Array with the shape of the detector plane.
        """
        if self.from_date is None or self.to_date is None:
            return 0
        if val == "mean":
            return self.inp_dt.mean
        elif val == "sigma":
            return self.inp_dt.std
        elif val == "skewness":
            return self.inp_dt.skewness
        elif val == "kurtosis":
            return self.inp_dt.kurtosis
        else:
            raise Exception("Failed val in get_math_value()")

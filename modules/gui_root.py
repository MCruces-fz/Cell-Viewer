from modules.parent_gui import CellsApp
from utils.tkinter_modules import *
import datetime


class CellsAppROOT(CellsApp):
    def __init__(self, chef_object: object, window_title=None):
        super().__init__(chef_object, window_title)
        self.var_hour_from = None
        self.var_mins_from = None
        self.var_hour_to = None
        self.var_mins_to = None

    def choose_options(self):
        super().choose_options()

        self.var_hour_from = tk.IntVar(value=0)
        self.var_mins_from = tk.IntVar(value=0)
        self.var_hour_to = tk.IntVar(value=0)
        self.var_mins_to = tk.IntVar(value=0)

        spx_hour_from = tk.Spinbox(self.frm_datime, from_=0, to=23, width=2, wrap=True, textvariable=self.var_hour_from)
        spx_mins_from = tk.Spinbox(self.frm_datime, from_=0, to=59, width=2, wrap=True, textvariable=self.var_mins_from)
        spx_hour_to = tk.Spinbox(self.frm_datime, from_=0, to=23, width=2, wrap=True, textvariable=self.var_hour_to)
        spx_mins_to = tk.Spinbox(self.frm_datime, from_=0, to=59, width=2, wrap=True, textvariable=self.var_mins_to)

        spx_hour_from.grid(row=1, column=2)
        spx_mins_from.grid(row=1, column=3)
        spx_hour_to.grid(row=2, column=2)
        spx_mins_to.grid(row=2, column=3)

    def grid_button(self, master, i, j, bg_color="#000000", fg_color="#ffffff"):
        # super().grid_button(master, i, j, )
        button_obj = tk.Button(master=master,
                               text=f"{self.get_math_value(val=self.choice_math_val.get())[i, j]:.3f}",
                               height=2, width=4,
                               bg=bg_color, fg=fg_color,
                               command=lambda a=i, b=j: self.cell_button(a, b))
        return button_obj

    def update_datetime(self):
        self.from_date = datetime.datetime.combine(
            self.cal_from.get_date(),
            datetime.time(hour=self.var_hour_from.get(), minute=self.var_mins_from.get())
        )
        self.to_date = datetime.datetime.combine(
            self.cal_to.get_date(),
            datetime.time(hour=self.var_hour_to.get(), minute=self.var_mins_to.get())
        )

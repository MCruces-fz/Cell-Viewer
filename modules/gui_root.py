from modules.parent_gui import CellsApp
import matplotlib.pyplot as plt
from utils.tkinter_modules import *
import datetime


class CellsAppROOT(CellsApp):
    def __init__(self, chef_object: object, window_title=None, theme: str = "dark"):
        super().__init__(chef_object, window_title, theme)
        self.var_hour_from = None
        self.var_mins_from = None
        self.var_hour_to = None
        self.var_mins_to = None

    def set_spinbox(self, master, var, f=0, t=1):
        spx = tk.Spinbox(master, from_=f, to=t, width=2,
                         wrap=True, textvariable=var,
                         bg=self.bg_default, fg=self.fg_default,
                         buttonbackground=self.bg_default, bd=0)
        return spx

    def choose_options(self):
        super().choose_options()
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

    def grid_button(self, master, i, j, bg_color="#000000", fg_color="#ffffff"):
        # super().grid_button(master, i, j, )
        value_name = self.choice_math_val.get()
        if value_name == "mean":
            txt = f"{self.get_math_value(val=value_name)[i, j]:.1f} Hz"
        else:
            txt = f"{self.get_math_value(val=value_name)[i, j]:.0f}"

        button_obj = tk.Button(master=master,
                               text=txt,
                               height=2, width=4,
                               bg=bg_color, fg=fg_color,
                               command=lambda a=i, b=j: self.cell_button(a, b), bd=0)
        return button_obj

    def cell_button(self, row_id, col_id):
        pass

    def update_datetime(self):
        self.from_date = datetime.datetime.combine(
            self.cal_from.get_date(),
            datetime.time(hour=self.var_hour_from.get(), minute=self.var_mins_from.get())
        )
        self.to_date = datetime.datetime.combine(
            self.cal_to.get_date(),
            datetime.time(hour=self.var_hour_to.get(), minute=self.var_mins_to.get())
        )

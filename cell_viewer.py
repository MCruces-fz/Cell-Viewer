"""
@author: MCruces

-----------------------------------------
Sources:

The Real Python
https://realpython.com/python-gui-tkinter/#working-with-widgets

Command Buttons
https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
"""
import numpy as np
from tkinter_modules import tk, DateEntry
import os
from os.path import join as join_path
import datetime
import matplotlib.pyplot as plt

DATA_DIR = "/home/mcruces/Documents/fptrucha_hits/png/"


class CookData:
    def __init__(self, data_dir: str = DATA_DIR, from_date=None, to_date=None,
                 plane_name: str = "T1", plane_rows: int = 10, plane_cols: int = 12):
        self.main_data_dir = data_dir

        self.from_date = from_date
        self.to_date = to_date

        self.plane_name = plane_name
        self.plane_rows = plane_rows
        self.plane_cols = plane_cols

        self.dir_1, self.dir_2 = self.set_full_rate_paths()

        self.all_data = self.read_data()
        self.mean = self.all_data.mean(axis=0)
        self.std = self.all_data.std(axis=0)

    def set_full_rate_paths(self):
        dir_1 = self.from_date.strftime("%y%j")
        dir_2 = self.to_date.strftime("%y%j")

        path_1 = join_path(join_path(self.main_data_dir, dir_1), "rate")
        path_2 = join_path(join_path(self.main_data_dir, dir_2), "rate")

        return path_1, path_2

    def read_data(self):
        # FIXME: Error across years
        folder_1 = self.from_date.strftime("%y%j")
        folder_2 = self.to_date.strftime("%y%j")

        arys = []
        for doy in range(int(folder_1), int(folder_2) + 1):
            rate_path = join_path(join_path(self.main_data_dir, str(doy)), "rate")
            try:
                list_dir = os.listdir(rate_path)
            except FileNotFoundError:
                raise Exception("Saved data is missing for this date range!")
            for filename in list_dir:
                if filename.endswith("_cell_entries.dat"):
                    arys.append(self.get_each_array(join_path(rate_path, filename)))
        return np.asarray(arys)

    def get_each_array(self, full_path):

        plane_indices = {"T1": 0, "T3": 1, "T4": 2}
        position = plane_indices[self.plane_name]
        init = position * (self.plane_rows + 1) + 1
        fin = init + self.plane_rows

        with open(full_path, "r+") as f:
            lines = f.readlines()[init:fin]
        ary = np.asarray([list(map(int, line.split("\t")[:-1])) for line in lines])
        return ary


cook_debug = False
if __name__ == "__main__" and cook_debug:
    from_d = datetime.date(year=2020, month=11, day=27)
    to_d = datetime.date(year=2020, month=12, day=9)

    cook_data = CookData(data_dir=DATA_DIR, from_date=from_d, to_date=to_d, plane_name="T1", plane_rows=10,
                         plane_cols=12)
    print(cook_data.mean.shape)
    print(cook_data.std.shape)


class CellsApp:
    def __init__(self, window_title=None, data_dir: str = DATA_DIR):
        self.window = tk.Tk()
        self.window_config(window_title)

        self.main_data_dir = data_dir

        self.plane_rows = 10
        self.plane_cols = 12

        # D A T A - N E E D E D
        self.plane_name = "T1"
        self.all_data = None
        self.mean = None
        self.std = None

        # D A T E S - F R A M E
        self.from_date = None
        self.to_date = None
        self.ok_var = tk.IntVar()
        self.frm_cells = None

        self.choose_dates()

        # M A I N - L O O P
        self.main_loop()

    def choose_dates(self):
        frm_dates = tk.Frame(master=self.window)
        frm_dates.pack(fill=tk.X, expand=True)

        lbl_dates = tk.Label(master=frm_dates, text='Choose dates:')
        lbl_dates.grid(row=0, column=0, columnspan=2)

        lbl_from = tk.Label(master=frm_dates, text='From: ')
        cal_from = DateEntry(master=frm_dates, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
        lbl_to = tk.Label(master=frm_dates, text='To: ')
        cal_to = DateEntry(master=frm_dates, width=12, background='darkblue',
                           foreground='white', borderwidth=2)

        btn_draw = tk.Button(master=frm_dates, text="Ok",
                             command=lambda a=cal_from, b=cal_to: self.refresh_cells(a, b))

        option_list = ["T1", "T3", "T4"]
        choice_var = tk.StringVar(master=frm_dates)
        choice_var.set(option_list[0])
        opt_plane_name = tk.OptionMenu(frm_dates, choice_var, *option_list)

        lbl_from.grid(row=1, column=0)
        cal_from.grid(row=1, column=1)
        lbl_to.grid(row=2, column=0)
        cal_to.grid(row=2, column=1)
        opt_plane_name.grid(row=1, column=2, rowspan=2)
        btn_draw.grid(row=1, column=3, rowspan=2)

        frm_dates.wait_variable(self.ok_var)
        self.plane_name = choice_var.get()

    def draw_cells(self):
        self.frm_cells = tk.Frame(master=self.window)
        self.frm_cells.pack(fill=tk.BOTH, expand=True)

        tk.Grid.rowconfigure(self.frm_cells, index=list(range(self.plane_rows)), weight=1, minsize=0)
        tk.Grid.columnconfigure(self.frm_cells, index=list(range(self.plane_cols)), weight=1, minsize=0)

        for i in range(self.plane_rows):
            for j in range(self.plane_cols):
                frm_cell = tk.Frame(
                    master=self.frm_cells,
                    # relief=tk.RAISED,
                    borderwidth=0
                )
                frm_cell.grid(row=i, column=j)

                mean, std = self.get_mean(i, j), self.get_std(i, j)
                btn_plot = tk.Button(master=frm_cell,
                                     text=f"{mean:.1f}\n\xB1{std:.1f}",
                                     height=2, width=3,
                                     command=lambda a=i, b=j: self.cell_button(a, b))
                btn_plot.pack(fill=tk.BOTH)

    def refresh_cells(self, cal_from, cal_to):
        self.ok_var.set(1)

        self.from_date = cal_from.get_date()
        self.to_date = cal_to.get_date()

        cooked_data = CookData(data_dir=self.main_data_dir,
                               from_date=self.from_date, to_date=self.to_date,
                               plane_name=self.plane_name,
                               plane_rows=self.plane_rows, plane_cols=self.plane_cols)
        self.all_data = cooked_data.all_data
        self.mean = cooked_data.mean
        self.std = cooked_data.std

        try:
            self.frm_cells.destroy()
        except AttributeError:
            pass
        self.draw_cells()

    def cell_button(self, row_id, col_id):
        
        all_hits = self.all_data[:, row_id, col_id]
        mean = self.mean[row_id, col_id]
        std = self.std[row_id, col_id]

        plt.figure(f"cell ({row_id}, {col_id})")
        plt.title(f"Cell ({row_id}, {col_id})")

        plt.hist(all_hits, color='c', edgecolor='k', alpha=0.65)
        plt.axvline(mean, color='k', linestyle='dashed', linewidth=1, label=f'Mean: {mean:.2f}')
        min_ylim, max_ylim = plt.ylim()
        plt.errorbar(x=mean, y=max_ylim * 0.5, xerr=std * 0.5, color='k', label=f'Std.: {std:.2f}')

        plt.xlabel("Number of hits")
        plt.ylabel("Counts")
        plt.legend(loc="best")

        plt.show()

    def get_mean(self, row_id, col_id):
        if self.from_date is None or self.to_date is None:
            return 0
        else:
            return self.mean[row_id, col_id]

    def get_std(self, row_id, col_id):
        if self.from_date is None or self.to_date is None:
            return 0
        else:
            return self.std[row_id, col_id]

    def window_config(self, window_title):
        if window_title is None:
            self.window.title("Cell Viewer")
        else:
            self.window.title(window_title)

    def main_loop(self):
        self.window.mainloop()


full_debug = True
if __name__ == "__main__" and full_debug:
    CellsApp()

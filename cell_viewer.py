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
from scipy.stats import kurtosis, skew
from tkinter_modules import tk, DateEntry
import os
from os.path import join as join_path
import datetime

from matplotlib import cm
from matplotlib.colors import Normalize, to_hex
import matplotlib.pyplot as plt

DATA_DIR = "/home/mcruces/Documents/fptrucha_hits/png/"


# TODO:
#    - Quitar decimales de los númros en las celdas
#    - Formato de fecha dd/mm/yy
#    - Color en función de STD. y quitarla de los
#    botones para mayor visibilidad
#    - Cambiar color map a arcoiris
#    - En un futuro hacer más botones para escoger
#    distintas cofiguracioes de colores y datos mostrados

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
        self.kurtosis = kurtosis(self.all_data, axis=0)
        self.symmetry = skew(self.all_data, axis=0)  # skew = 0 -> 100% symmetric

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
        # self.data_range = None
        self.mapper = None

        self.mean = None
        self.std = None
        self.kurtosis = None
        self.symmetry = None
        self.choice_math_val = None

        # D A T E S - F R A M E
        self.from_date = None
        self.to_date = None
        self.ok_var = tk.IntVar()
        self.frm_cells = None
        self.choice_plane_var = None
        self.choice_cmap = None

        self.choose_dates()

        # M A I N - L O O P
        self.main_loop()

    def choose_dates(self):
        frm_dates = tk.Frame(master=self.window)
        frm_dates.pack(fill=tk.X, expand=True)

        lbl_dates = tk.Label(master=frm_dates, text='Choose dates \"dd/mm/yyyy\":')

        lbl_from = tk.Label(master=frm_dates, text='From: ')
        cal_from = DateEntry(master=frm_dates, width=12, background='red', date_pattern="dd/mm/yyyy",
                             foreground='white', borderwidth=2)

        lbl_to = tk.Label(master=frm_dates, text='To: ')
        cal_to = DateEntry(master=frm_dates, width=12, background='green', date_pattern="dd/mm/yyyy",
                           foreground='white', borderwidth=2)

        btn_draw = tk.Button(master=frm_dates, text="Ok",
                             command=lambda a=cal_from, b=cal_to: self.refresh_cells(a, b))

        lbl_plane = tk.Label(master=frm_dates, text="Plane: ")
        option_list_plane = ["T1", "T3", "T4"]
        self.choice_plane_var = tk.StringVar(master=frm_dates)
        self.choice_plane_var.set(option_list_plane[0])
        opt_plane_name = tk.OptionMenu(frm_dates, self.choice_plane_var, *option_list_plane)

        lbl_var_color = tk.Label(master=frm_dates, text="Variable to color: ")
        option_list_var = ["mean", "deviation", "kurtosis", "symmetry"]
        self.choice_math_val = tk.StringVar(master=frm_dates)
        self.choice_math_val.set(option_list_var[0])
        opt_variable_color = tk.OptionMenu(frm_dates, self.choice_math_val, *option_list_var)

        lbl_cmap = tk.Label(master=frm_dates, text="Color map: ")
        option_list_cmap = ["jet", "inferno", "plasma", "Pastel2",
                            "copper", "cool", "gist_rainbow",
                            "viridis", "winter", "twilight"]
        self.choice_cmap = tk.StringVar(master=frm_dates)
        self.choice_cmap.set(option_list_cmap[1])
        opt_variable_cmap = tk.OptionMenu(frm_dates, self.choice_cmap, *option_list_cmap)

        lbl_dates.grid(row=0, column=0, columnspan=2)
        lbl_from.grid(row=1, column=0)
        cal_from.grid(row=1, column=1)
        lbl_to.grid(row=2, column=0)
        cal_to.grid(row=2, column=1)

        lbl_plane.grid(row=0, column=2)
        opt_plane_name.grid(row=1, column=2, rowspan=2)

        lbl_var_color.grid(row=0, column=3)
        opt_variable_color.grid(row=1, column=3, rowspan=2)

        lbl_cmap.grid(row=0, column=4)
        opt_variable_cmap.grid(row=1, column=4, rowspan=2)

        btn_draw.grid(row=1, column=5, rowspan=2)

        frm_dates.wait_variable(self.ok_var)

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
                frm_cell.grid(row=i, column=j, sticky="news")

                # mean, std = self.get_mean(i, j), self.get_std(i, j)

                numpy_value = self.get_math_value(val=self.choice_math_val.get())[i, j]
                bg_color, fg_color = self.set_button_colors(numpy_value)
                btn_plot = tk.Button(master=frm_cell,
                                     text=f"{self.get_math_value(val='mean')[i, j]:.0f}"
                                          f"\n\xB1"
                                          f"{self.get_math_value(val='deviation')[i, j]:.0f}",
                                     height=2, width=3,
                                     bg=bg_color, fg=fg_color,
                                     command=lambda a=i, b=j: self.cell_button(a, b))
                btn_plot.pack(fill=tk.BOTH)

    def set_button_colors(self, val: float):
        # Management of background color (button)
        var_array = self.get_math_value(val=self.choice_math_val.get())
        rgba_color = self.mapper.to_rgba(val)
        bg_color = to_hex(rgba_color[:-1])

        # Management of foreground color (words)
        condition = np.min(var_array) <= val < np.mean(var_array)
        # dark on high values
        if self.choice_cmap.get() in ["inferno", "copper", "viridris", "winter", "jet", "plasma", "viridis"]:
            if condition:
                fg_color = "#FFFFFF"
            else:
                fg_color = "#000000"
        # light on high values
        elif self.choice_cmap.get() in ["cool", "twilight"]:
            if condition:
                fg_color = "#000000"
            else:
                fg_color = "#FFFFFF"
        else:
            fg_color = "#000000"

        return bg_color, fg_color

    def refresh_cells(self, cal_from, cal_to):
        self.ok_var.set(1)

        self.from_date = cal_from.get_date()
        self.to_date = cal_to.get_date()

        self.plane_name = self.choice_plane_var.get()

        # TODO: Crear un método update para CookData en el que se metan estos valores,
        #  pero inicializarlo en CellViewer.__init__() para poder acceder a sus valores
        #  en cualquier parte de CellViewer sin necesidad de definir self.mean, self.std...
        cooked_data = CookData(data_dir=self.main_data_dir,
                               from_date=self.from_date, to_date=self.to_date,
                               plane_name=self.plane_name,
                               plane_rows=self.plane_rows, plane_cols=self.plane_cols)
        self.all_data = cooked_data.all_data

        self.mean = cooked_data.mean
        self.std = cooked_data.std
        self.kurtosis = cooked_data.kurtosis
        self.symmetry = cooked_data.symmetry

        # normalize item number values to colormap
        numpy_value = self.get_math_value(val=self.choice_math_val.get())
        norm = Normalize(vmin=np.min(numpy_value), vmax=np.max(numpy_value))
        self.mapper = cm.ScalarMappable(norm=norm, cmap=self.choice_cmap.get())

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
        plt.title(f"Plane {self.plane_name} - Cell index ({row_id}, {col_id})")

        plt.hist(all_hits, color='c', edgecolor='k', alpha=0.65)
        plt.axvline(mean, color='k', linestyle='dashed', linewidth=1, label=f'Mean: {mean:.2f}')
        min_ylim, max_ylim = plt.ylim()
        plt.errorbar(x=mean, y=max_ylim * 0.68, xerr=std, color='k', label=f'Std.: {std:.2f}')

        plt.xlabel("Number of hits")
        plt.ylabel("Counts")
        plt.legend(loc="best")

        plt.show()

    '''
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

    def get_kurtosis(self, row_id, col_id):
        if self.from_date is None or self.to_date is None:
            return 0
        else:
            return self.kurtosis[row_id, col_id]

    def get_symmetry(self, row_id, col_id):
        if self.from_date is None or self.to_date is None:
            return 0
        else:
            return self.symmetry[row_id, col_id]
    '''

    def get_math_value(self, val: str) -> np.array:
        if self.from_date is None or self.to_date is None:
            return 0
        if val == "mean":
            return self.mean
        elif val == "deviation":
            return self.std
        elif val == "kurtosis":
            return self.kurtosis
        elif val == "symmetry":
            return self.symmetry
        else:
            raise Exception("Failed val in get_math_value()")

    def window_config(self, window_title):
        if window_title is None:
            self.window.title("Cell Viewer")
        else:
            self.window.title(window_title)

    def main_loop(self):
        self.window.mainloop()


if __name__ == "__main__":
    CellsApp()

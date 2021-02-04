import numpy as np
from utils.tkinter_modules import tk, DateEntry

from matplotlib import cm
from matplotlib.colors import Normalize, to_hex
import matplotlib.pyplot as plt
from utils.const import DATA_DIR
from modules.cook_ascii import CookData


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
        self.skewness = None
        self.choice_math_val = None

        # D A T E S - F R A M E
        self.from_date = None
        self.to_date = None
        self.ok_var = tk.IntVar()
        self.frm_cells = None
        self.frm_colormap = None
        self.choice_plane_var = None
        self.choice_cmap = None

        self.choose_dates()

        # M A I N - L O O P
        self.main_loop()

    def choose_dates(self):
        """
        This sets the frame where the buttons to choose options are placed.
        """
        # FRAME THAT ENCLOSES  E V E R Y T H I N G  E L S E  (all options)
        frm_options = tk.Frame(master=self.window)
        frm_options.pack(fill=tk.X, expand=True)

        # CHOOSE DATE-TIME OPTIONS
        # Label: "Choose dates 'dd/mm/yyyy'"
        lbl_dates = tk.Label(master=frm_options, text='Choose dates \"dd/mm/yyyy\":')

        # Entry "From" date
        lbl_from = tk.Label(master=frm_options, text='From: ')
        cal_from = DateEntry(master=frm_options, width=12, background='red', date_pattern="dd/mm/yyyy",
                             foreground='white', borderwidth=2)

        # Entry "To" date
        lbl_to = tk.Label(master=frm_options, text='To: ')
        cal_to = DateEntry(master=frm_options, width=12, background='green', date_pattern="dd/mm/yyyy",
                           foreground='white', borderwidth=2)

        lbl_plane = tk.Label(master=frm_options, text="Plane: ")
        option_list_plane = ["T1", "T3", "T4"]
        self.choice_plane_var = tk.StringVar(master=frm_options)
        self.choice_plane_var.set(option_list_plane[0])
        opt_plane_name = tk.OptionMenu(frm_options, self.choice_plane_var, *option_list_plane)

        lbl_var_color = tk.Label(master=frm_options, text="Variable to color: ")
        option_list_var = ["mean", "sigma", "kurtosis", "skewness"]
        self.choice_math_val = tk.StringVar(master=frm_options)
        self.choice_math_val.set(option_list_var[0])
        opt_variable_color = tk.OptionMenu(frm_options, self.choice_math_val, *option_list_var)

        lbl_cmap = tk.Label(master=frm_options, text="Color map: ")
        option_list_cmap = ["jet", "inferno", "plasma", "Pastel2",
                            "copper", "cool", "gist_rainbow",
                            "viridis", "winter", "twilight"]
        self.choice_cmap = tk.StringVar(master=frm_options)
        self.choice_cmap.set(option_list_cmap[0])
        opt_variable_cmap = tk.OptionMenu(frm_options, self.choice_cmap, *option_list_cmap)

        # OK Button!
        btn_draw = tk.Button(master=frm_options, text="Ok",
                             command=lambda a=cal_from, b=cal_to: self.refresh_cells(a, b))

        # - G R I D -
        lbl_dates.grid(row=0, column=0, columnspan=2)
        lbl_from.grid(row=1, column=0)
        cal_from.grid(row=1, column=1)
        lbl_to.grid(row=2, column=0)
        cal_to.grid(row=2, column=1)

        lbl_plane.grid(row=3, column=0)
        opt_plane_name.grid(row=4, column=0, rowspan=2)

        lbl_var_color.grid(row=3, column=1)
        opt_variable_color.grid(row=4, column=1, rowspan=2)

        lbl_cmap.grid(row=3, column=2)  # (row=0, column=4)
        opt_variable_cmap.grid(row=4, column=2, rowspan=2)

        btn_draw.grid(row=6, column=0, columnspan=3)

        # Wait while self.refresh_cells() method is not executed (pressing "Ok" button)
        frm_options.wait_variable(self.ok_var)

    # def draw_colormap_bar(self):
    #     """
    #     This sets the frame where the buttons to choose options are placed.
    #     """
    #     # FRAME THAT ENCLOSES  E V E R Y T H I N G  E L S E  (all options)
    #     self.frm_colormap = tk.Frame(master=self.window)
    #     self.frm_colormap.pack(fill=tk.X, expand=True)
    #
    #     plt.figure()
    #     fig, ax = plt.subplots()
    #     fig.colorbar(self.mapper, ax=ax, orientation="horizontal")  # , fraction=0.046, pad=0.04)
    #     ax.remove()
    #     canvas = FigureCanvasTkAgg(master=self.frm_colormap, figure=fig)  # (fig, master)
    #
    #     canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_colormap_bar(self, min, max):
        """
        This sets the frame where the buttons to choose options are placed.
        """
        # FRAME THAT ENCLOSES  E V E R Y T H I N G  E L S E  (all options)
        self.frm_colormap = tk.Frame(master=self.window)
        self.frm_colormap.pack(fill=tk.X, expand=True)

        step = int((max - min)/20)
        min, max = int(min), int(max)

        for val in range(min, max, step):
            rgba_color = self.mapper.to_rgba(val)
            rgb_color = rgba_color[:-1]
            bg_color = to_hex(rgb_color)
            tk.Label(master=self.frm_colormap, bg=bg_color).pack(fill=tk.X, expand=True, side=tk.RIGHT)

    def draw_cells(self):
        """
        This sets the frame where the cell buttons are placed
        """
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
                                     text=f"{self.get_math_value(val=self.choice_math_val.get())[i, j]:.0f}",
                                     height=2, width=4,
                                     bg=bg_color, fg=fg_color,
                                     command=lambda a=i, b=j: self.cell_button(a, b))
                if j != 5 and i != 4:
                    btn_plot.pack(fill=tk.BOTH, expand=True)
                elif j == 5 and i != 4:
                    v_sep = tk.Label(master=frm_cell, text="   ")
                    btn_plot.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
                    v_sep.pack(fill=tk.BOTH, side=tk.RIGHT)
                elif i == 4 and j != 5:
                    h_sep = tk.Label(master=frm_cell)
                    btn_plot.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
                    h_sep.pack(fill=tk.BOTH, side=tk.BOTTOM)
                else:  # i == 4 and j == 5
                    v_sep = tk.Label(master=frm_cell, text="   ")
                    h_sep = tk.Label(master=frm_cell)
                    # btn_plot.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
                    btn_plot.grid(row=0, column=0)
                    v_sep.grid(row=0, column=1)
                    h_sep.grid(row=1, column=0)

    def set_button_colors(self, val: float):
        """
        This method is used for choose the color for each value in the cell buttons.
        :param val: Value of each button.
        :return: Colors for button background (bg_color) and button value (fg_color)
        """
        # Management of background color (button)
        rgba_color = self.mapper.to_rgba(val)
        rgb_color = rgba_color[:-1]
        bg_color = to_hex(rgb_color)

        # Management of foreground color (words)
        inv_rgb_color = (1 - rgb_color[0], 1 - rgb_color[1], 1 - rgb_color[2])
        fg_color = to_hex(inv_rgb_color)  # Foreground is inverted color of background

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
        self.skewness = cooked_data.skewness

        # normalize item number values to colormap
        numpy_value = self.get_math_value(val=self.choice_math_val.get())
        min = np.min(numpy_value)
        max = np.max(numpy_value)
        norm = Normalize(vmin=min, vmax=max)
        self.mapper = cm.ScalarMappable(norm=norm, cmap=self.choice_cmap.get())

        try:
            self.frm_cells.destroy()
        except AttributeError:
            pass
        try:
            self.frm_colormap.destroy()
        except AttributeError:
            pass

        self.draw_cells()
        self.draw_colormap_bar(min, max)

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
        plt.yscale("log")

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
            return self.skewness[row_id, col_id]
    '''

    def get_math_value(self, val: str) -> np.array:
        if self.from_date is None or self.to_date is None:
            return 0
        if val == "mean":
            return self.mean
        elif val == "sigma":
            return self.std
        elif val == "skewness":
            return self.skewness
        elif val == "kurtosis":
            return self.kurtosis
        else:
            raise Exception("Failed val in get_math_value()")

    def window_config(self, window_title):
        if window_title is None:
            self.window.title("Cell Viewer")
        else:
            self.window.title(window_title)

    def main_loop(self):
        self.window.mainloop()
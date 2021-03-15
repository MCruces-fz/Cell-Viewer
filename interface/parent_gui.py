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
from utils.tkinter_modules import tk, ttk, DateEntry

from matplotlib import cm
from matplotlib.colors import Normalize, to_hex
from utils.const import *

from kitchen.chef import Chef


class CellsApp:
    def __init__(self, chef_object: Chef, window_title=None, theme: str = "dark"):
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

        #  --- L A Y O U T ---
        # M A I N   W I N D O W
        self.window = tk.Tk()
        # Configuration:
        self.theme = theme
        self.bg_default = None
        self.fg_default = None
        self.window_config(window_title)

        # Object of Input Data
        self.inp_dt = chef_object

        # W I D G E T S
        # --- Frames:
        self.frm_options = tk.Frame(master=self.window, bg=self.bg_default)
        self.frm_datime = tk.Frame(master=self.frm_options, bg=self.bg_default)
        self.frm_display = None
        self.frm_cells = None
        self.frm_colormap = None
        # --- Labels:
        # self.lbl_date = None

        #     V A R I A B L E
        # D E C L A R A T I O N S
        # datetime objects:
        self.from_date = None
        self.to_date = None
        # Tk Calendars:
        self.cal_from = None
        self.cal_to = None
        # Colormap:
        self.mapper = None
        self.choice_cmap = None
        # Other variables:
        self.plane_name = "T1"
        self.choice_math_val = None
        self.choice_plane_var = None
        self.ok_var = tk.IntVar()

        # L O G I C
        # Initiates first widget:
        self.choose_options()
        # Wait while self.refresh_cells method is not executed
        # Continue pressing "Ok" button
        self.frm_options.wait_variable(self.ok_var)

        # M A I N - L O O P
        self.main_loop()

    def choose_options(self):
        """
        L A Y O U T

        This sets the frame where the buttons to choose options are placed.
        """

        # FRAME THAT ENCLOSES   E V E R Y T H I N G   E L S E  (all options)
        self.frm_options.pack(fill=tk.X, expand=True)

        # CHOOSE DATE-TIME OPTIONS
        # Label: "Choose dates 'dd/mm/yyyy'"
        lbl_date = tk.Label(master=self.frm_datime, text='Date dd/mm/yyyy',
                            bg=self.bg_default, fg=self.fg_default)

        # Entry "From" date
        lbl_from = tk.Label(master=self.frm_datime, text='From: ',
                            bg=self.bg_default, fg=self.fg_default)
        self.cal_from = DateEntry(master=self.frm_datime, width=12,
                                  background='red', date_pattern="dd/mm/yyyy",
                                  foreground='white', borderwidth=2,
                                  style='my.DateEntry')

        # Entry "To" date
        lbl_to = tk.Label(master=self.frm_datime, text='To: ',
                          bg=self.bg_default, fg=self.fg_default)
        self.cal_to = DateEntry(master=self.frm_datime, width=12,
                                background='green', date_pattern="dd/mm/yyyy",
                                foreground='white', borderwidth=2,
                                style='my.DateEntry')

        # CHOOSE PLANE NAME
        lbl_plane = tk.Label(master=self.frm_options, text="Plane: ",
                             bg=self.bg_default, fg=self.fg_default)
        option_list_plane = ["T1", "T3", "T4"]
        self.choice_plane_var = tk.StringVar(master=self.frm_options)
        self.choice_plane_var.set(option_list_plane[0])
        opt_plane_name = tk.OptionMenu(self.frm_options, self.choice_plane_var, *option_list_plane)
        opt_plane_name.config(bg=self.bg_default, fg=self.fg_default, bd=0)

        # CHOOSE VARIABLE TO SHOW
        lbl_var_color = tk.Label(master=self.frm_options, text="Variable to color: ",
                                 bg=self.bg_default, fg=self.fg_default)
        option_list_var = self.inp_dt.option_list_var  #
        self.choice_math_val = tk.StringVar(master=self.frm_options)
        self.choice_math_val.set(option_list_var[0])
        opt_variable_color = tk.OptionMenu(self.frm_options, self.choice_math_val, *option_list_var)
        opt_variable_color.config(bg=self.bg_default, fg=self.fg_default, bd=0)

        # CHOOSE COLORMAP
        lbl_cmap = tk.Label(master=self.frm_options, text="Color map: ",
                            bg=self.bg_default, fg=self.fg_default)
        option_list_cmap = ["jet", "inferno", "plasma", "Pastel2",
                            "copper", "cool", "gist_rainbow",
                            "viridis", "winter", "twilight"]
        self.choice_cmap = tk.StringVar(master=self.frm_options)
        self.choice_cmap.set(option_list_cmap[0])
        opt_variable_cmap = tk.OptionMenu(self.frm_options, self.choice_cmap, *option_list_cmap)
        opt_variable_cmap.config(bg=self.bg_default, fg=self.fg_default, bd=0)

        # OK Button!
        btn_draw = tk.Button(master=self.frm_options, text="Ok",
                             command=self.refresh_cells, bg=self.bg_default, fg=self.fg_default, bd=0)

        # - G R I D -
        self.frm_datime.grid(row=0, column=0, rowspan=3, columnspan=4)
        lbl_date.grid(row=0, column=0, columnspan=2)
        lbl_from.grid(row=1, column=0)
        self.cal_from.grid(row=1, column=1)
        lbl_to.grid(row=2, column=0)
        self.cal_to.grid(row=2, column=1)

        lbl_plane.grid(row=3, column=0)
        opt_plane_name.grid(row=4, column=0, rowspan=2)

        lbl_var_color.grid(row=3, column=1)
        opt_variable_color.grid(row=4, column=1, rowspan=2)

        lbl_cmap.grid(row=3, column=2)  # (row=0, column=4)
        opt_variable_cmap.grid(row=4, column=2, rowspan=2)

        btn_draw.grid(row=6, column=0, columnspan=3)

    def refresh_cells(self):
        """
        Action fot the OK button. It must refresh all cell buttons if necessary
        """
        self.ok_var.set(1)
        self.update_datetime()
        self.plane_name = self.choice_plane_var.get()

        self.inp_dt.update(from_date=self.from_date, to_date=self.to_date,
                           plane_name=self.plane_name, var_to_update=self.choice_math_val.get())

        # normalize item number values to colormap
        numpy_value = self.get_math_value(val=self.choice_math_val.get())
        min_val = np.min(numpy_value)
        max_val = np.max(numpy_value)
        norm = Normalize(vmin=min_val, vmax=max_val)
        self.mapper = cm.ScalarMappable(norm=norm, cmap=self.choice_cmap.get())

        try:
            self.frm_display.destroy()
        except AttributeError:
            pass

        self.draw_cells()
        self.draw_colormap_bar(min_val, max_val)

    def update_datetime(self):
        """
        Needs to be edited by the developer!
        """
        raise Exception("Method update_datetime must be override")

    def draw_cells(self):
        """
        This sets the frame where the cell buttons are placed
        """
        self.frm_display = tk.Frame(master=self.window, bg=self.bg_default)
        self.frm_display.pack(fill=tk.BOTH, expand=True)

        self.frm_cells = tk.Frame(master=self.frm_display, bg=self.bg_default)
        self.frm_cells.grid(row=0, column=0, sticky="news")

        tk.Grid.rowconfigure(self.frm_cells, index=list(range(NROW)), weight=1, minsize=0)
        tk.Grid.columnconfigure(self.frm_cells, index=list(range(NCOL)), weight=1, minsize=0)

        for i in range(NROW):
            for j in range(NCOL):
                frm_cell = tk.Frame(
                    master=self.frm_cells,
                    # relief=tk.RAISED,
                    borderwidth=0,
                    bg=self.bg_default
                )
                frm_cell.grid(row=i, column=j, sticky="news")

                # mean, std = self.get_mean(i, j), self.get_std(i, j)

                numpy_value = self.get_math_value(val=self.choice_math_val.get())[i, j]
                bg_color, fg_color = self.set_button_colors(numpy_value)
                btn_plot = self.grid_button(master=frm_cell,
                                            i=i, j=j,
                                            bg_color=bg_color, fg_color=fg_color)

                if j != 5 and i != 4:
                    btn_plot.pack(fill=tk.BOTH, expand=True)
                elif j == 5 and i != 4:
                    v_sep = tk.Label(master=frm_cell, text="   ", bg=self.bg_default, fg=self.fg_default)
                    btn_plot.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
                    v_sep.pack(fill=tk.BOTH, side=tk.RIGHT)
                elif i == 4 and j != 5:
                    h_sep = tk.Label(master=frm_cell, bg=self.bg_default, fg=self.fg_default)
                    btn_plot.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
                    h_sep.pack(fill=tk.BOTH, side=tk.BOTTOM)
                else:  # i == 4 and j == 5
                    v_sep = tk.Label(master=frm_cell, text="   ", bg=self.bg_default, fg=self.fg_default)
                    h_sep = tk.Label(master=frm_cell, bg=self.bg_default, fg=self.fg_default)
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

    def grid_button(self, master, i, j, bg_color="#000000", fg_color="#ffffff") -> tk.Button:
        """
        Tkinter Button object, prepared for stack on the grid.

        :param master: Parent frame
        :param i: Index of the row
        :param j: Index of the column
        :param bg_color: (optional) background color
        :param fg_color: (optional) foreground color.
        :return: tk.Button object
        """
        raise Exception("Method grid_button must be override.")

    def draw_colormap_bar(self, min_val, max_val):
        """
        This sets the frame where the buttons to choose options are placed.
        """
        # FRAME THAT ENCLOSES  E V E R Y T H I N G  E L S E  (all options)
        self.frm_colormap = tk.Frame(master=self.frm_display, bg=self.bg_default, width=500)
        self.frm_colormap.grid(row=0, column=1, columnspan=3, sticky="news", ipadx=10, padx=5)

        steps_number = 20
        step_size = (max_val - min_val) / steps_number

        for step in range(steps_number):
            val = min_val + step_size * step
            rgba_color = self.mapper.to_rgba(val)
            rgb_color = rgba_color[:-1]
            bg_color = to_hex(rgb_color)
            tk.Label(master=self.frm_colormap, bg=bg_color).pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

    def get_math_value(self, val: str) -> np.array:
        """
        Function which returns the array corresponding to the given string.

        :param val: String with the name of the desired array.
        :return: Array with the shape of the detector plane.
        """
        raise Exception("Method get_math_value must be override")

    def window_config(self, window_title):
        if self.theme == "light":
            self.bg_default = "#ffffff"
            self.fg_default = "#303030"
        else:
            self.bg_default = "#303030"
            self.fg_default = "#ffffff"

        self.window.configure(bg=self.bg_default)

        style = ttk.Style(self.window)
        # create custom DateEntry style with red background
        style.configure('my.DateEntry',
                        fieldbackground=self.bg_default, fieldforeground=self.fg_default,
                        background=self.bg_default, foreground=self.fg_default)

        if window_title is None:
            self.window.title("Cell Viewer")
        else:
            self.window.title(window_title)

    def main_loop(self):
        self.window.mainloop()
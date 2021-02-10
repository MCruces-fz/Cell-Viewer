from modules.parent_gui import CellsApp
import matplotlib.pyplot as plt
from utils.tkinter_modules import tk


class CellsAppASCII(CellsApp):
    def update_datetime(self):
        self.from_date = self.cal_from.get_date()
        self.to_date = self.cal_from.get_date()

    def grid_button(self, master, i, j, bg_color="#000000", fg_color="#ffffff"):
        button_obj = tk.Button(master=master,
                               text=f"{self.get_math_value(val=self.choice_math_val.get())[i, j]:.0f}",
                               height=2, width=4,
                               bg=bg_color, fg=fg_color,
                               command=lambda a=i, b=j: self.cell_button(a, b), bd=0)
        return button_obj

    def cell_button(self, row_id, col_id):
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

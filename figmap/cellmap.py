"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Author: Miguel Cruces Fernández
e-mail:
  - miguel.cruces.fernandez@usc.es
  - mcsquared.fz@gmail.com
"""

from kitchen.cook_root import CookDataROOT

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import to_hex, Normalize
from os.path import join as join_path


class Cellmap:
    """
    Matplotlibilization of the cell map.
    """
    storage_dir = "store/saves/"
    fig = None

    def __init__(self):
        # , cooked: CookDataROOT, plane_name: str,
        # save: bool = True, show: bool = False):

        self.plane_name = None
        self._mapper = None
        self.cooked = None
        self.save_cm = True
        self.show_cm = False
        self.hz = False

        self.filename = None

    @property
    def mapper(self):
        return self._mapper

    @mapper.setter
    def mapper(self, mapper: cm.ScalarMappable):
        self._mapper = mapper

    def create(self):
        if len(self.cooked.used_filenames) > 1:
            files_str = f"{self.cooked.used_filenames[0]}-{self.cooked.used_filenames[-1]}"
        else:
            files_str = f"{self.cooked.used_filenames[0]}"

        self.filename = f"{files_str}-"\
                        f"{self.plane_name}-"\
                        f"{self.cooked.current_var}"

        title = f"Plane: {self.plane_name}, Branch: {self.cooked.current_var}\n"\
                f"Files: {files_str}"

        self.fig, (cells, cmap) = plt.subplots(
            ncols=2,
            figsize=(7, 5),
            gridspec_kw={
                "width_ratios": [15, 1]
            }
        )
        self.fig.tight_layout()
        cells.axis("off")
        # cmap.tick_params(labelrotation=315)
        cmap.tick_params(labelrotation=270)

        c_min, c_max = self.mapper.get_clim()
        im = cells.matshow(
            self.cooked.plane_event,
            interpolation=None,
            aspect='auto',
            cmap=self.mapper.get_cmap(),
            vmin=c_min, vmax=c_max,
        )

        cipher = lambda n: int(np.log10(n) + 1)

        for (i, j), z in np.ndenumerate(self.cooked.plane_event):
            if not self.hz:
                txt = f"{z}"
                if z >= 1e2:
                    font_size = 32 / cipher(z)
                else:
                    font_size = 12
            else:
                txt = f"{z:.3f}"
                font_size = 9

            _, foreground = self.set_value_color(z)
            cells.text(
                j, i,
                txt,
                fontsize=font_size,
                ha="center", va="center",
                color=foreground
            )

        cells.set_title(title)
        # ax1.set_ylabel('Blah2')
        self.fig.colorbar(im, cmap)

    def set_mapper(self, set_max: bool = False, max_val: float = 0.8, cmap_name: str = "jet"):
        """
        Normalize item number values to colormap.
        Create a matplotlib.cm.ScalarMappable called self.mapper.

        (min, max) = self.mapper.get_clim()
        color_map = self.mapper.get_cmap()
        """
        numpy_value = self.cooked.plane_event
        try:
            if set_max:
                # TODO: Choose max_val
                min_val = 0
                max_val = float(max_val)
            else:
                min_val = np.min(numpy_value)
                max_val = np.max(numpy_value)
        except Exception:  # FIXME: Better exception, please!
            min_val = np.min(numpy_value)
            max_val = np.max(numpy_value)
        norm = Normalize(vmin=min_val, vmax=max_val)
        self.mapper = cm.ScalarMappable(norm=norm, cmap=cmap_name)

    def set_value_color(self, val: float):
        """
        This method is used for choose the color for each value in the cell buttons.
        :param val: Value of each button.
        :return: Colors for button background (bg_color) and button value (fg_color)
        """

        # Management of background color (button)
        rgba_color = self._mapper.to_rgba(val)
        rgb_color = rgba_color[:-1]
        bg_color = to_hex(rgb_color)

        # Management of foreground color (words)
        inv_rgb_color = (1 - rgb_color[0], 1 - rgb_color[1], 1 - rgb_color[2])
        fg_color = to_hex(inv_rgb_color)  # Foreground is inverted color of background

        return bg_color, fg_color

    def save_file(self, ext: str = "png", create: bool = True):
        if create:
            self.create()

        if ext.startswith("."):
            ext = ext[1:]

        self.fig.savefig(
            f"{join_path(self.storage_dir, self.filename)}.{ext}",
            bbox_inches='tight'
        )

    def update(self, cooked: CookDataROOT, plane_name: str,
               save: bool = True, show: bool = False, hz: bool = False):
        self.plane_name = plane_name
        self.cooked = cooked
        self.save_cm = save
        self.show_cm = show
        self.hz = hz

        if self._mapper is None:
            self.set_mapper()

        self.filename = f"fromdate-todate-planename-branch-{np.random.random() * 100:.0f}"

    @classmethod
    def execute(cls, cooked: CookDataROOT, mapper: cm.ScalarMappable, plane_name: str,
                save: bool = True, show: bool = False):
        """
        Save the current cell map

        :param cooked: Cooked data from an instnce of a class that inherits from Chef.
        :param mapper: Color map object created in an instance of a class that inherits from CellsApp.
        :param plane_name: Name of the plane to analyze, i.e. "T1", "T3", "T4".
        :param save: True (default) to save_cm the file, False to skip.
        :param show: True to show_cm cellmap, False (default) to not.
        """
        cellmap = cls(cooked, mapper, plane_name)
        cellmap.create()

        if save:
            cellmap.save_file("png")
        if show:
            # FIXME: It Doesn't work...
            cellmap.fig.show()

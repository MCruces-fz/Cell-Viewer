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

        self._mapper = None
        self.cooked = None
        self.save_cm = True
        self.show_cm = False
        self.hz = False

        self.filename = None

    def update(self, cooked: CookDataROOT, save: bool = True,
               show: bool = False, hz: bool = False):
        """
        Update the current cell map

        :param cooked: Cooked data from an instnce of a class that inherits from Chef.
        :param save: True (default) to save_cm the file, False to skip.
        :param show: True to show_cm cellmap, False (default) to not.
        :param hz: True to show cellmap in Hz units, False (default) to show it
            in default units (number of counts).
        """
        self.cooked = cooked
        self.save_cm = save
        self.show_cm = show
        self.hz = hz

        if self._mapper is None:
            self.set_mapper()

    @property
    def mapper(self):
        """
        Mapper Getter
        """
        return self._mapper

    @mapper.setter
    def mapper(self, mapper: cm.ScalarMappable):
        """
        Mapper setter
        """
        self._mapper = mapper

    def create(self):
        """
        Create the Cellmap
        """
        # Title and Filename:
        if len(self.cooked.used_filenames) > 1:
            files_str = f"{self.cooked.used_filenames[0]}-{self.cooked.used_filenames[-1]}"
        else:
            files_str = f"{self.cooked.used_filenames[0]}"

        self.filename = f"{files_str}-"\
                        f"{self.cooked.plane_name}-"\
                        f"{self.cooked.current_var}"

        title = f"Plane: {self.cooked.plane_name}, Branch: {self.cooked.current_var}\n"\
                f"Files: {files_str}"

        # Create Figure:
        self.fig, (cells, cmap) = plt.subplots(
            ncols=2,
            figsize=(7, 5),
            gridspec_kw={
                "width_ratios": [15, 1]
            }
        )
        self.fig.tight_layout()

        # Cellmap:
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

        cells.plot([5.5, 5.5], [-0.5, 9.5], "#ffffff")
        cells.plot([-0.5, 11.5], [4.5, 4.5], "#ffffff")

        cells.axis("off")
        cells.set_title(title)

        # Color map bar:
        c_min, c_max = self.mapper.get_clim()
        im = cells.matshow(
            self.cooked.plane_event,
            interpolation=None,
            aspect='auto',
            cmap=self.mapper.get_cmap(),
            vmin=c_min, vmax=c_max,
        )

        cmap.tick_params(labelrotation=270)
        self.fig.colorbar(im, cmap)

    def set_mapper(self, set_max: bool = False, max_val: float = 0.8, cmap_name: str = "jet"):
        """
        Normalize item number values to colormap.
        Create a matplotlib.cm.ScalarMappable called self.mapper.

        (min, max) = self.mapper.get_clim()
        color_map = self.mapper.get_cmap()

        :param set_max: True to set a maximum value in color map, False (default) to
            calculate maximum automatically.
        :param max_val: If set_max=True, max_val is the maximum value to set maximum
            color in cellmap.
        :param cmap_name: Name of the Color Map Gradient.
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

    def save_file(self, out_path: str = None, ext: str = "png", re_create: bool = True, label: str = ""):
        """
        Save the created figure.

        :param out_path: Path to to the directory to save the file.
        :param ext: Extension of the output file.
        :param re_create: True to create the figure again (default), False to use de previous
            calculated figure. If any figure exists, it will raise an error.
        :param label: Label to the end of the filename (optional).
        """
        if re_create:
            self.create()

        if ext.startswith("."):
            ext = ext[1:]

        if out_path is None:
            out_path = self.storage_dir

        self.fig.savefig(
            f"{join_path(out_path, self.filename)}{label}.{ext}",
            bbox_inches='tight'
        )

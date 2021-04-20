"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

"""

from kitchen.cook_root import CookDataROOT

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from os.path import join as join_path


class Cellmap:
    """
    Matplotlibilization of the cell map.
    """
    storage_dir = "store/saves/"

    @classmethod
    def save(cls, cooked: CookDataROOT, mapper: cm.ScalarMappable, plane_name: str,
             save: bool = True, show: bool = False):
        """
        Save the current cell map

        :param cooked:
        :param mapper:
        :param plane_name:
        :param save:
        :param show:
        :return:
        """
        filename = f"fromdate-todate-planename-branch-{np.random.random() * 100:.0f}"
        title = f"{cls.storage_dir}, plane: {plane_name}, branch: {cooked.current_var}"

        fig, (cells, cmap) = plt.subplots(
            ncols=2,
            figsize=(14, 10),
            gridspec_kw={
                "width_ratios": [12, 1]
            }
        )

        c_min, c_max = mapper.get_clim()
        im = cells.matshow(
            cooked.plane_event,
            interpolation=None,
            aspect='auto',
            cmap=mapper.get_cmap(),
            vmin=c_min, vmax=c_max,
        )

        cells.set_title(title)
        # ax1.set_ylabel('Blah2')
        fig.colorbar(im, cmap)

        if save:
            fig.savefig(f"{join_path(cls.storage_dir, filename)}.png")
        if show:
            fig.show()

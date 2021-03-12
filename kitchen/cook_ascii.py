"""
@author: MCruces

"""

import numpy as np
import os
from os.path import join as join_path
from scipy.stats import kurtosis, skew
from typing import List

from kitchen.chef import Chef
from utils.const import *


class CookDataASCII(Chef):
    def __init__(self, data_dir: str = ASCII_DATA_DIR):
        """
        Constructor for the ASCII files chef.

        :param data_dir: Parent directory where ASCII files are stored.
        """
        super().__init__(data_dir)

        self._option_list_var: List[str] = ["mean", "sigma", "kurtosis", "skewness"]

    def get_hits_array(self, full_path):
        """
        Get array from ASCII file with hits un tables for the plane
        called self.plane_name.

        :param full_path: Full path to the needed file
        :return: Numpy array with hits in the self.plane_name plane
        """

        # FIXME: Make it more generic.
        plane_indices = {"T1": 0, "T3": 1, "T4": 2}
        position = plane_indices[self.plane_name]
        init = position * (NROW + 1) + 1
        fin = init + NROW

        with open(full_path, "r") as f:
            lines = f.readlines()[init:fin]
        ary = np.asarray([list(map(int, line.split("\t")[:-1])) for line in lines])
        return ary

    def read_data(self):
        """
        Redefinition of Chef.read_data() method to read data from
        ASCII files.

        :return: Numpy array with all data.
        """

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
                    arys.append(self.get_hits_array(join_path(rate_path, filename)))
        return np.asarray(arys)

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1", var_to_update: str = None):
        super().update(from_date, to_date, plane_name)

        self.all_data = self.read_data()

        self.mean = self.all_data.mean(axis=0)
        self.std = self.all_data.std(axis=0)
        self.kurtosis = kurtosis(self.all_data, axis=0)
        self.skewness = skew(self.all_data, axis=0)

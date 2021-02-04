import numpy as np
import os
from os.path import join as join_path

from modules.chef import Chef
from utils.const import *


class CookDataASCII(Chef):
    def __init__(self, data_dir: str = DATA_DIR):
        super().__init__(data_dir)

        # DECLARE MORE VARIABLES
        self.dir_1 = None
        self.dir_2 = None

    def get_each_array(self, full_path):
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

    def set_full_rate_paths(self):
        dir_1 = self.from_date.strftime("%y%j")
        dir_2 = self.to_date.strftime("%y%j")

        path_1 = join_path(join_path(self.main_data_dir, dir_1), "rate")
        path_2 = join_path(join_path(self.main_data_dir, dir_2), "rate")

        return path_1, path_2

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1"):
        super().update(from_date, to_date, plane_name)

        self.dir_1, self.dir_2 = self.set_full_rate_paths()

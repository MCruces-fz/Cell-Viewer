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

import numpy as np
import os
from os.path import join as join_path
from scipy.stats import kurtosis, skew
from typing import List

from kitchen.chef import Chef
from utils.const import NROW
from utils.dirs import ASCII_DATA_DIR


class CookDataASCII(Chef):
    def __init__(self, data_dir: str = ASCII_DATA_DIR):
        """
        Constructor for the ASCII files chef.

        :param data_dir: Parent directory where ASCII files are stored.
        """
        super().__init__(data_dir)

        self._option_list_var: List[str] = ["mean", "sigma", "kurtosis", "skewness"]
        self.current_var = self._option_list_var[0]

        self.mean = None
        self.std = None
        self.skewness = None  # skew = 0 -> 100% symmetric
        self.kurtosis = None

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
        """
        Method to update all the self variables needed for the ASCII GUI.

        :param from_date: Starting date in datetime format.
        :param to_date: Ending date in datetime format.
        :param plane_name: Name of the plane to get values.
        :param var_to_update:
        :return: Void function, It only updates self variables.
        """
        # super().update(from_date, to_date, plane_name)

        # Update all data only if necessary
        if from_date != self.from_date or to_date != self.to_date or \
                plane_name != self.plane_name or var_to_update != self.current_var:

            self.from_date = from_date
            self.to_date = to_date
            self.plane_name = plane_name
            self.current_var = var_to_update

            self.all_data = self.read_data()

            self.mean = self.all_data.mean(axis=0)
            self.std = self.all_data.std(axis=0)
            self.kurtosis = kurtosis(self.all_data, axis=0)
            self.skewness = skew(self.all_data, axis=0)

            self.plane_event = dict(zip(
                self._option_list_var,
                [self.mean, self.std, self.kurtosis, self.skewness]
            ))[self.current_var]

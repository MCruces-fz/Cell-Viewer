"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Author: Miguel Cruces Fernández
e-mail:
  - miguel.cruces.fernandez@usc.es
  - mcsquared.fz@gmail.com
"""

import numpy as np
from typing import List


class Chef:
    def __init__(self, data_dir: str):
        """
        Constructor for the parent class CHEF
        Chef is the object whom cooks data.

        :param data_dir: Prent directory with all data.
        """

        self.main_data_dir = data_dir

        # DECLARE VARIABLES
        self.from_date = None
        self.to_date = None

        self.plane_name = None

        self.all_data = None

        self._option_list_var: List[str] = []

    @property
    def option_list_var(self):
        return self._option_list_var

    def read_data(self) -> np.array:
        """
        EDIT IS NEEDED:

        Method to read all the hit data from wherever it is
        stored, in whatever format is needed

        :return: 3D Numpy array with all data.
        """

        raise Exception("Method read_data must be override")

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1", var_to_update: str = None):
        """
        Method to update all the self variables needed for the GUI.

        :param from_date: Starting date in datetime format.
        :param to_date: Ending date in datetime format.
        :param plane_name: Name of the plane to get values.
        :param var_to_update:
        :return: Void function, It only updates self variables.
        """

        # Update all data only if necessary
        if from_date != self.from_date or to_date != self.to_date or \
                plane_name != self.plane_name:

            self.from_date = from_date
            self.to_date = to_date

            self.plane_name = plane_name

            # self.mean     =  MEAN
            # self.std      =  STD
            # self.kurtosis =  KURTOSIS
            # self.skewness =  SKEWNESS

"""
@author: MCruces

"""

import numpy as np


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
        self.mean = None
        self.std = None
        self.skewness = None  # skew = 0 -> 100% symmetric
        self.kurtosis = None

    def read_data(self):
        """
        EDIT IS NEEDED:

        Method to read all the hit data from wherever it is
        stored, in whatever format is needed

        :return: 3D Numpy array with all data.
        """
        return np.array([])

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1"):
        """
        Method to update all the self variables needed for the GUI.

        :param from_date: Starting date in datetime format.
        :param to_date: Ending date in datetime format.
        :param plane_name: Name of the plane to get values.
        :return: Void function, It only updates self variables.
        """

        # Update all data only if necessary
        if from_date != self.from_date or to_date != self.to_date or \
                plane_name != self.plane_name:

            self.from_date = from_date
            self.to_date = to_date

            self.plane_name = plane_name

            self.all_data = self.read_data()

            # self.mean     =  MEAN
            # self.std      =  STD
            # self.kurtosis =  KURTOSIS
            # self.skewness =  SKEWNESS

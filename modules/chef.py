import numpy as np
from scipy.stats import kurtosis, skew
from utils.const import DATA_DIR


class Chef:
    def __init__(self, data_dir: str = DATA_DIR):

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
        Edit is needed

        :return: Numpy array
        """
        return np.array([])

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1"):

        self.from_date = from_date
        self.to_date = to_date

        self.plane_name = plane_name

        self.all_data = self.read_data()
        self.mean = self.all_data.mean(axis=0)
        self.std = self.all_data.std(axis=0)
        self.kurtosis = kurtosis(self.all_data, axis=0)
        self.skewness = skew(self.all_data, axis=0)

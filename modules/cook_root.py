import numpy as np
from utils.const import *
from modules.chef import Chef


class CookDataROOT(Chef):
    def __init__(self, data_dir: str = DATA_DIR):
        super().__init__(data_dir)

    def read_data(self):
        pass

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1"):
        super().update(from_date, to_date, plane_name)

#!/usr/bin/python3
"""
@author: MCruces

"""

# from modules.cells_app import CellsApp
from modules.cook_root import CookDataROOT
from utils.const import DATA_DIR


if __name__ == "__main__":
    cook_data = CookDataROOT(data_dir=DATA_DIR)
    # CellsApp(chef_object=cook_data)

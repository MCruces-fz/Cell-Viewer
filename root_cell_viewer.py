#!/usr/bin/python3
"""
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

@author: MCruces

"""

from interface.gui_root import CellsAppROOT
from kitchen.cook_root import CookDataROOT
from utils.dirs import ROOT_DATA_DIR

cook_data = CookDataROOT(data_dir=ROOT_DATA_DIR)
# ary = cook_data.read_data()
CellsAppROOT(chef_object=cook_data, theme="dark")

# TODO:
#  Extraer todos los archivos ascii y guardarlos en:
#  Datos4TB/tragaldabas/data/monitoring/cellmaps
#  con nombres más cortitos y útiles

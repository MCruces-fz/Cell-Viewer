#!/usr/bin/python3
"""
@author: MCruces

"""

from os.path import join as join_path
from modules.gui_root import CellsAppROOT
from modules.cook_root import CookDataROOT
from utils.const import ROOT_DATA_DIR, TRUFA_LIB_DIR
from ROOT import gSystem

trufa_lib_path = join_path(TRUFA_LIB_DIR, "libtunpacker.so")
gSystem.Load(trufa_lib_path)

cook_data = CookDataROOT(data_dir=ROOT_DATA_DIR)
# ary = cook_data.read_data()
CellsAppROOT(chef_object=cook_data, theme="dark")

# TODO:
#  Extraer todos los archivos ascii y guardarlos en:
#  Datos4TB/tragaldabas/data/monitoring/cellmaps
#  con nombres más cortitos y útiles

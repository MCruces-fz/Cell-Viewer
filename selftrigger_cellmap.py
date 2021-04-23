from kitchen.cook_root import CookDataROOT
from figmap.cellmap import Cellmap

# import argparse

cooked = CookDataROOT()
cellmap = Cellmap()

filename = "tr21109103527.hld.root.root"

cooked.current_var = "RAW"
cooked.check_m1 = False
cooked.check_hz = False

for plane in ["T1", "T3", "T4"]:
    cooked.plane_name = plane

from kitchen.cook_root import CookDataROOT
from figmap.cellmap import Cellmap
from utils.const import FILE_PLANE

# import argparse
from os.path import join as join_path

cooked = CookDataROOT()
cellmap = Cellmap()

file_path = join_path(
    "/home/mcruces/Documents/fptrucha_hits/selftrigger/ST088/",
    "st21105115619.hld.root.root"
)

cooked.current_var = "RAW"
cooked.check_m1 = False
cooked.check_hz = False
cooked.plane_name = FILE_PLANE[file_path.split("/")[-2]]

cooked.get_raw_hits_array(file_path)

cellmap.update(cooked)
cellmap.save_file(out_path=None, ext="png")

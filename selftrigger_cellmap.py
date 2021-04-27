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

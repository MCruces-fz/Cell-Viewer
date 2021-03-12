"""
@author: MCruces

    # rdf = RDataFrame(tree)
    # # rpc_hit = rdf.GetLeaf("rpchit.fX")
    # # IMPORTANT
    # # https://www.reddit.com/r/learnpython/comments/7ivlid/translation_from_root_to_pyroot/
    # # https://pastebin.com/8ixEe34h
    # # https://root-forum.cern.ch/t/no-ttree-asmatrix-and-rdataframe-in-experimental-pyroot/36184
    # # https://root.cern/doc/master/pyroot002__TTreeAsMatrix_8py.html
    # # ary = rpc_hit.AsMatrix()
    # ary = rdf.AsNumpy()
    # print(ary)

    # # ??
    # gStyle.SetOptStat(1000000001)

    # # Create TCanvas:
    # #    This is the window TCanvas("c", "c", width, height)
    # # https://root.cern.ch/root/html532/TCanvas.html
    # can = TCanvas("can", "can", 1100, 700)

    # # Divide the canvas in 3 columns and 2 rows
    # can.Divide(3, 2, 0.01, 0.01)

    # # Draw this in the first TPad of the can TCanvas
    # can.cd(1)
    # can.Draw("rpcraw.fRow-1:rpcraw.fCol-1>>T1(12,0,12,10,0,10)",
    #          "rpcraw.fTrbnum==2", "colz text")
    # can.cd(2)
    # can.Draw("rpcraw.fRow-1:rpcraw.fCol-1>>T3(12,0,12,10,0,10)",
    #          "rpcraw.fTrbnum==0", "colz text")
"""

import datetime
import numpy as np
import os
from os.path import join as join_path
from utils.const import *
from kitchen.chef import Chef
import root_numpy as rnp
from ROOT import gROOT, gSystem, TFile, kTRUE, TCanvas, RDataFrame, gStyle
from ROOT import EnableImplicitMT  # Multi Thread

from typing import List


class CookDataROOT(Chef):
    def __init__(self, data_dir: str = ROOT_DATA_DIR):
        """
        Constructor for the ROOT files chef.

        :param data_dir: Parent directory where ROOT files are stored.
        """
        super().__init__(data_dir)

        gSystem.Load(join_path(TRUFA_LIB_DIR, "libtunpacker.so"))

        # FIXME : choose adecuate dtype
        self.all_data = np.zeros((NROW, NCOL), dtype=np.uint32)
        self.total_diff_time = None

        self._option_list_var: List[str] = ["hits", "Hz", "saetas"]
        self.current_var: str = self._option_list_var[0]

    def read_data(self) -> np.array:
        """
        Redefinition of Chef.read_data() method to read data from
        ROOT files.

        :return: Numpy array with all data.
        """
        # What the hack is this?
        gROOT.SetBatch(kTRUE)
        EnableImplicitMT()

        file_from = self.from_date.strftime("%y%j%H%M%S")
        file_to = self.to_date.strftime("%y%j%H%M%S")

        tstamp_from = int(file_from)
        tstamp_to = int(file_to)

        # Clear Data
        self.all_data = np.zeros((NROW, NCOL), dtype=np.uint32)

        for filename in sorted(os.listdir(ROOT_DATA_DIR)):
            if not filename.endswith('.root'): continue
            tstamp_file = int(filename[2:2 + len(file_from)])
            if tstamp_from <= tstamp_file <= tstamp_to:
                self.get_hits_array(join_path(self.main_data_dir, filename))
                print(f"{(tstamp_file - tstamp_from) / (tstamp_to - tstamp_from) * 100 :.2f}%\tdone")
        print("100%\tdone")

        return self.all_data

    def get_hits_array(self, full_path):
        # Create TFile
        file0 = TFile(full_path, "READ")
        # Read TTree
        tree = file0.Get("T")
        # nentries = tree.GetEntries()

        trbnum = TRB_TAB[self.plane_name]
        col_branch = rnp.tree2array(tree=tree,
                                    branches="rpcraw.fCol",
                                    selection=f"rpcraw.fTrbnum == {trbnum}")
        row_branch = rnp.tree2array(tree=tree,
                                    branches="rpcraw.fRow",
                                    selection=f"rpcraw.fTrbnum == {trbnum}")

        self.all_data, _, _ = np.histogram2d(
            np.concatenate(row_branch),
            np.concatenate(col_branch),
            bins=[
                np.arange(0.5, NROW + 1),
                np.arange(0.5, NCOL + 1)
            ]
        )

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1", var_to_update: str = None):
        # super().update(from_date, to_date, plane_name)

        # Update all data only if necessary
        if from_date != self.from_date or to_date != self.to_date or \
                plane_name != self.plane_name or var_to_update != self.current_var:
            self.from_date = from_date
            self.to_date = to_date
            self.plane_name = plane_name

            if var_to_update != self.current_var:
                if var_to_update == "hits":
                    self.all_data = self.read_data()
                elif var_to_update == "Hz":
                    self.all_data = self.read_data()

                    # FIXME: It won't work if there is missing data in range (mean will be wrong)
                    #  IDEA: cuenta el número de archivos y estima el tiempo a partir de ahí
                    self.total_diff_time = self.to_date - self.from_date
                    self.mean = self.all_data / self.total_diff_time.total_seconds()
                elif var_to_update == "saetas":
                    pass

            self.current_var = var_to_update

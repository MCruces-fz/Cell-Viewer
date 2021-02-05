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
from modules.chef import Chef
import ROOT
import root_numpy as rnp
from ROOT import gROOT, gStyle, TFile, kTRUE, TCanvas, RDataFrame
from ROOT import EnableImplicitMT  # Multi Thread


class CookDataROOT(Chef):
    def __init__(self, data_dir: str = ROOT_DATA_DIR):
        """
        Constructor for the ROOT files chef.

        :param data_dir: Parent directory where ROOT files are stored.
        """
        super().__init__(data_dir)

        # FIXME : choose adecuate dtype
        self.all_data = np.zeros((NROW, NCOL), dtype=np.uint32)

    def read_data(self):
        """
        Redefinition of Chef.read_data() method to read data from
        ROOT files.

        :return: Numpy array with all data.
        """
        # ??
        gROOT.SetBatch(kTRUE)
        EnableImplicitMT()

        # Take range of dates
        # find files and get its full paths
        # use get_hits_array() method to get arrays and append them into one greater array

        # TODO: implementar una función para escoger las dfechas y otra para escoger las horas
        #  Como argumento obligatorio deben tener el frame en el que se debe acomodar

        # Delete when finished
        # self.from_date = datetime.datetime(year=2020, month=4, day=3, hour=12, minute=30)
        # self.to_date = datetime.datetime(year=2020, month=4, day=3, hour=15, minute=23)

        file_from = self.from_date.strftime("%y%j%H%M")
        file_to = self.to_date.strftime("%y%j%H%M")

        tstamp_from = int(file_from)
        tstamp_to = int(file_to)

        # Clear Data
        self.all_data = np.zeros((NROW, NCOL), dtype=np.uint32)

        for filename in sorted(os.listdir(ROOT_DATA_DIR)):
            tstamp_file = int(filename[2:2 + len(file_from)])
            if tstamp_from <= tstamp_file <= tstamp_to:
                # Input Filename
                input_full_path = join_path(self.main_data_dir, filename)
                self.get_hits_array(input_full_path)
                print(f"{(tstamp_file - tstamp_from) / (tstamp_to - tstamp_from) * 100 :.2f}%\tdone")
        print("100%\tdone")

        return self.all_data

    def get_hits_array(self, full_path):
        # Delete when finished
        self.plane_name = "T1"

        # Create TFile
        file0 = TFile(full_path, "READ")

        # Read TTree
        tree = file0.Get("T")

        nentries = tree.GetEntries()
        # print(f"Number of entries: {nentries}")

        trbnum = TRB_TAB[self.plane_name]
        # print(trbnum)

        col_branch = rnp.tree2array(tree=tree,
                                    branches="rpcraw.fCol",
                                    selection=f"rpcraw.fTrbnum == {trbnum}")
        row_branch = rnp.tree2array(tree=tree,
                                    branches="rpcraw.fRow",
                                    selection=f"rpcraw.fTrbnum == {trbnum}")

        col_arr = np.concatenate(col_branch)
        row_arr = np.concatenate(row_branch)

        coord_hits = np.vstack((row_arr, col_arr)).T
        # print(coord_hits.shape)

        # FIXME: Find more efficient way!!
        for coords in coord_hits:
            row, col = coords
            self.all_data[row - 1, col - 1] += 1

        # print(self.all_data)

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1"):
        super().update(from_date, to_date, plane_name)

        # FIXME: It won't work if there is missing data in range (mean will be wrong)
        #  IDEA: cuenta el número de archivos y estima el tiempo a partir de ahí
        time_diff = self.to_date - self.from_date
        self.mean = self.all_data / time_diff.total_seconds()

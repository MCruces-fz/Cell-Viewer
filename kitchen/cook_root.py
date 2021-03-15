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
from utils.const import NROW, NCOL, TRB_TAB, ROOT_DATA_DIR, TRUFA_LIB_DIR
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
                if self.current_var == "saetas":
                    pass
                    # self.all_data = np.zeros((NCOL, NROW))
                elif self.current_var in ["hits", "Hz"]:
                    self.get_raw_hits_array(join_path(self.main_data_dir, filename))
                print(f"{(tstamp_file - tstamp_from) / (tstamp_to - tstamp_from) * 100 :.2f}%\tdone")
        print("100%\tdone")

        return self.all_data

    def get_rpc_saeta_array(self, full_path:str):
        """
        Set all hits used in reconstruction in chosen detector plane to all_data
        attribute of this class.

        :param full_path: full path to the root file.
        """

        # TODO: Leer la rama RpcSaeta3Planes y para cada saeta de cada evento tomar las coordenadas
        #  de los hits usados para reconstruir dicha saeta.

        # Read TTree
        file0 = TFile(full_path, "READ")
        tree = file0.Get("T")

        nevents = tree.GetEntries()

        debug = True

        if debug:
            plane_name = "T1"
            self.plane_name = plane_name

        trbnum = TRB_TAB[self.plane_name]

        for evt in range(nevents):
            tree.GetEntry(evt)

            ind_leaf = tree.GetLeaf(f"RpcSaeta3Planes.find{trbnum}")

            nsaetas = ind_leaf.GetLen()
            if not nsaetas: continue

            if debug:
                print(f"{nsaetas}\t#Saetas")

            col_leaf = tree.GetLeaf("rpchit.fCol")
            row_leaf = tree.GetLeaf("rpchit.fRow")
            nhits = col_leaf.GetLen()

            if debug:
                trb_leaf = tree.GetLeaf("rpchit.fTrbnum")
                print(f"{nhits}\t#Hits")

                trb_nhits = 0
                for hit in range(trb_leaf.GetLen()):
                    plane = trb_leaf.GetValue(hit)
                    if plane == trbnum:
                        trb_nhits += 1
                print(f"{trb_nhits}\t#Hits in plane {self.plane_name}")


            k_indices = []
            saetas_per_index = {}
            for entry in range(nsaetas):
                k_ind = int(ind_leaf.GetValue(entry))
                if debug:
                    if not k_ind in k_indices:
                        k_indices.append(k_ind)
                if not k_ind in saetas_per_index:
                    saetas_per_index[k_ind] = 0
                saetas_per_index[k_ind] += 1

            if debug:
                print(f"Hit indices in plane {self.plane_name}: {k_indices}")
                print(f"Saetas per index: {saetas_per_index}")
                print("")

            # col_leaf = []
            # row_leaf = []
            # for col, row in list(zip(col_leaf, row_leaf)):
            #     pass

    def get_raw_hits_array(self, full_path: str):
        """
        Set all hits in chosen detector plane to all_data attribute of this class.

        :param full_path: full path to the root file.
        """
        # Read TTree
        file0 = TFile(full_path, "READ")
        tree = file0.Get("T")
        # nentries = tree.GetEntries()

        trbnum = TRB_TAB[self.plane_name]
        # print(f"{self.plane_name}, trbnum = {trbnum}")
        col_branch = rnp.tree2array(tree=tree,
                                    branches="rpcraw.fCol",
                                    selection=f"rpcraw.fTrbnum == {trbnum}")
        row_branch = rnp.tree2array(tree=tree,
                                    branches="rpcraw.fRow",
                                    selection=f"rpcraw.fTrbnum == {trbnum}")

        hits, _, _ = np.histogram2d(
            np.concatenate(row_branch),
            np.concatenate(col_branch),
            bins=[
                np.arange(0.5, NROW + 1),
                np.arange(0.5, NCOL + 1)
            ]
        )

        self.all_data += hits.astype(np.uint32)

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1", var_to_update: str = None):
        # super().update(from_date, to_date, plane_name)

        # Update all data only if necessary
        if from_date != self.from_date or to_date != self.to_date or \
                plane_name != self.plane_name or var_to_update != self.current_var:
            self.from_date = from_date
            self.to_date = to_date
            self.plane_name = plane_name

            # if var_to_update != self.current_var:
            if var_to_update == "hits":
                self.all_data = self.read_data()
            elif var_to_update == "Hz":
                # FIXME: Fails when loading before saetas.
                self.all_data = self.read_data()

                # FIXME: It won't work if there is missing data in range (mean will be wrong)
                #  IDEA: cuenta el número de archivos y estima el tiempo a partir de ahí
                self.total_diff_time = self.to_date - self.from_date
                self.mean = self.all_data / self.total_diff_time.total_seconds()
            elif var_to_update == "saetas":
                pass

            self.current_var = var_to_update

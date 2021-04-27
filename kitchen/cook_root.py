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

# import datetime
import numpy as np
import os
from os.path import join as join_path
from utils.const import NROW, NCOL, TRB_TAB
from utils.dirs import ROOT_DATA_DIR, TRUFA_LIB_DIR
from utils.footilities import basename
from kitchen.chef import Chef
import root_numpy as rnp
from ROOT import gROOT, gSystem, TFile, kTRUE  # , TCanvas, RDataFrame, gStyle
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

        self.total_diff_time = None

        self._option_list_var: List[str] = ["RAW", "HIT", "SAETA"]
        self.current_var: str = self._option_list_var[0]

        self.plane_event = None

        self.check_m1 = False
        self.check_hz = False
        self.last_check_m1 = False
        self.last_check_hz = False

        self.used_filenames = []

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
        self.plane_event = np.zeros((NROW, NCOL), dtype=np.uint32)
        self.used_filenames = []

        for filename in sorted(os.listdir(ROOT_DATA_DIR)):
            if not filename.startswith(('tr', 'st')) or not filename.endswith('.root'): continue
            tstamp_file = int(filename[2:2 + len(file_from)])
            if tstamp_from <= tstamp_file <= tstamp_to:
                if self.current_var == "SAETA":
                    self.get_rpc_saeta_array(join_path(self.main_data_dir, filename))
                elif self.current_var in ["RAW", "HIT"]:
                    self.get_raw_hits_array(join_path(self.main_data_dir, filename))
                print(f"{(tstamp_file - tstamp_from) / (tstamp_to - tstamp_from) * 100 :.2f}%\tdone")
        print("100%\tdone")

    def get_rpc_saeta_array(self, full_path: str):
        """
        Set all hits used in reconstruction in chosen detector plane to plane_event
        attribute of this class.

        :param full_path: full path to the root file.
        """

        if self.plane_event is None:
            self.plane_event = np.zeros((NROW, NCOL), dtype=np.uint32)

        self.used_filenames.append(basename(full_path, extension=False))

        # Read TTree
        file0 = TFile(full_path, "READ")
        tree = file0.Get("T")

        nevents = tree.GetEntries()

        trbnum = TRB_TAB[self.plane_name]
        # reco_cells = np.zeros((NCOL, NROW))

        for evt in range(nevents):
            tree.GetEntry(evt)

            ind_leaf = tree.GetLeaf(f"RpcSaeta3Planes.find{trbnum}")

            nsaetas = ind_leaf.GetLen()
            if not nsaetas or (self.check_m1 and nsaetas != 1):
                continue

            col_leaf = tree.GetLeaf("rpchit.fCol")
            row_leaf = tree.GetLeaf("rpchit.fRow")
            nhits = col_leaf.GetLen()

            k_indices = []
            saetas_per_index = {}
            for entry in range(nsaetas):
                k_ind = int(ind_leaf.GetValue(entry))
                if k_ind not in saetas_per_index:
                    saetas_per_index[k_ind] = 0
                saetas_per_index[k_ind] += 1

            for hit in range(nhits):
                if hit in saetas_per_index:
                    hit = int(hit)
                    col = int(col_leaf.GetValue(hit))
                    row = int(row_leaf.GetValue(hit))
                    self.plane_event[row - 1, col - 1] += saetas_per_index[hit]

    def get_raw_hits_array(self, full_path: str):
        """
        Set all hits in chosen detector plane to plane_event attribute of this class.

        :param full_path: full path to the root file.
        """

        if self.plane_event is None:
            self.plane_event = np.zeros((NROW, NCOL), dtype=np.uint32)

        self.used_filenames.append(basename(full_path, extension=False))

        # Read TTree
        file0 = TFile(full_path, "READ")
        tree = file0.Get("T")

        if self.current_var == "HIT":
            branch = "rpchit"
        elif self.current_var == "RAW":
            branch = "rpcraw"
        else:
            raise Exception("Error choosing branch!")

        trbnum = TRB_TAB[self.plane_name]

        hits = np.zeros((NROW, NCOL))

        if self.check_m1:
            nevents = tree.GetEntries()
            for evt in range(nevents):
                tree.GetEntry(evt)

                col_leaf = tree.GetLeaf(f"{branch}.fCol")
                row_leaf = tree.GetLeaf(f"{branch}.fRow")
                trb_leaf = tree.GetLeaf(f"{branch}.fTrbnum")

                nhits = col_leaf.GetLen()

                if nhits != 3: continue

                hits_topo = [0, 0, 0]
                for k in range(nhits):
                    trb = trb_leaf.GetValue(k)
                    hits_topo[int(trb)] += 1

                if hits_topo != [1, 1, 1]: continue

                for k in range(nhits):
                    trb = trb_leaf.GetValue(k)
                    if trb == trbnum:
                        hits[int(row_leaf.GetValue(k) - 1), int(col_leaf.GetValue(k) - 1)] += 1

        else:
            col_branch = rnp.tree2array(tree=tree,
                                        branches=f"{branch}.fCol",
                                        selection=f"{branch}.fTrbnum == {trbnum}")
            row_branch = rnp.tree2array(tree=tree,
                                        branches=f"{branch}.fRow",
                                        selection=f"{branch}.fTrbnum == {trbnum}")

            hits, _, _ = np.histogram2d(
                np.concatenate(row_branch),
                np.concatenate(col_branch),
                bins=[
                    np.arange(0.5, NROW + 1),
                    np.arange(0.5, NCOL + 1)
                ]
            )

        self.plane_event += hits.astype(np.uint32)

    def update(self, from_date=None, to_date=None,
               plane_name: str = "T1", var_to_update: str = None):

        # Update all data only if necessary
        if from_date != self.from_date or to_date != self.to_date or \
                plane_name != self.plane_name or var_to_update != self.current_var or\
                self.last_check_m1 != self.check_m1 or self.last_check_hz != self.check_hz:
            self.from_date = from_date
            self.to_date = to_date
            self.plane_name = plane_name

            self.current_var = var_to_update
            self.read_data()
            if self.check_hz:
                # FIXME: It won't work if there is missing data in range (raw_hits_hz will be wrong)
                #  IDEA: cuenta el número de archivos y estima el tiempo a partir de ahí
                self.total_diff_time = self.to_date - self.from_date
                self.plane_event = self.plane_event / self.total_diff_time.total_seconds()

        self.last_check_m1 = self.check_m1
        self.last_check_hz = self.check_hz

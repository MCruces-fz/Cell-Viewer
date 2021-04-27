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

            ---------------------------
            C O N S T A N T S   F I L E
            ---------------------------
"""

# Number of rows and columns of each detector plane
NROW = 10
NCOL = 12

# TRB indices for each detector plane
TRB_TAB = {
    "T1": 2,
    "T3": 0,
    "T4": 1
}

TRB_CODE = {
    "T1": 88,
    "T3": 37,
    "T4": 71
}

ST_FILE = {
    "T1": "ST088",
    "T3": "ST037",
    "T4": "ST071"
}

FILE_PLANE = {
    "ST088": "T1",
    "ST037": "T3",
    "ST071": "T4"
}

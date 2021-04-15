# Cell Viewer
Graphical User Interface to view stats about the TRASGO detectors easily.

![Dark Theme](./store/screenshot.png) 

## How to use
You can check ascii files (`tryydoyhhmmss.hld_cell_entries.dat`) with `ascii_cell_viewer.py` or root files (`tryydoyhhmmss.hld.root.root`). First are faster to read and you can check the mean of hits in runs (around 25 minutes each run), with standard deviation, skewness and kurtosis; instead, reading root files you can measure a more accurate rate (in Hz).

### Set working directories
First you need to create the file `const/dirs.py` and add as UPPERCASE constants the following strings:
```python
# utils/const.py

ASCII_DATA_DIR = "/path/to/png/"
ROOT_DATA_DIR  = "/path/to/rootfiles/"
TRUFA_LIB_DIR  = "/path/to/libtunpacker.so"
```
where `ASCII_DATA_DIR` is the path to the directory where you have stored a copy from files in
```bash
fptrucha.usc.es:/home/labcaf/online/png/
```
`ROOT_DATA_DIR` is the path where you store unpacked files like:
```bash
tryydoyhhmmss.hld.root.root
# or
styydoyhhmmss.hld.root.root
```
and `TRUFA_LIB_DIR` is the path to the "TRUFA" compiled library.

### Install dependencies
You need to work with:
* Python >= 3.7
* Tkinter (`pip install tkinter`)
* ROOT >= 6.22
* PyROOT (for Python3)

### Run the program

Finally you need to execute
```bash
python3 ascii_cell_viewer.py
```
to read ascii files, or
```bash
python3 root_cell_viewer.py
```

I hope FPTrucha is not too busy, otherwise it will take him a bit to start the GUI...


## Motherboard disposition

### TRAGALDABAS
The motherboards are not in the same location as from the normal point 
of view, when you view TRAGALDABAS from the southwest (entering the door). 
Here are the cell layouts in both cases:

#### Motherboards on App:
They are in the same disposition that they are saved in ascii files.

| MB3 | MB2 |
|-----|-----|
| MB4 | MB1 |

#### Real disposition:
Below the table is the compass to locate you.

| MB2 | MB3 |
|-----|-----|
| MB2 | MB4 |

```
      N
       \
  ______\______ E
W  ------\-------
          \
           \
            S
|-------------------|
| - C O M P A S S - |
|-------------------|
```

```
         _______________________
       //                       \
      //       M I G U E L       \
     //        C R U C E S        \
    //                             \
   //                               \
  //       mcruces.fz@gmail.com      \
  \  miguel.cruces.fernandez@usc.es //
   \_______________________________//
```

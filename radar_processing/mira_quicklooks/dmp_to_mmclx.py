#!/home/camila/miniconda3/envs/amazon-storms-aerosols/bin/python

"""
Check .dmp files and convert to .mmclx
@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import sys
import subprocess
import time
from pathlib import Path
from glob import glob


# Defining path of data files
data_path = "/home/camila/git/amazon-storms-aerosols/data/radar/mira_campina/"

# Listing .dmp files
dmp_files = sorted(glob(data_path + "*/*/*/*.dmp", recursive=True))
# print(dmp_files)

# Listing .mmclx files
mmclx_files = sorted(glob(data_path + "*/*/*/*.mmclx", recursive=True))
# print(mmclx_files)

# Matching .dmp and .mmclx files
id = dmp_files.index(mmclx_files[-1][:-6] + ".dmp")
if id == len(dmp_files):
    sys.exit("No new files")
else:
    dmp_to_convert = dmp_files[id + 1]
    name_mmclx = dmp_files[id + 1][:-4] + ".mmclx"

    # Converting .dmp to .mmclx
    bt = time.time()
    subprocess.call(
        [
            "idl7sav mmclx_rho infile=",
            dmp_to_convert,
            "outfile=",
            name_mmclx,
            "melthei=4000",
        ]
    )
    print((time.time() - bt) / 60, "minutes to create", name_mmclx)


#!/home/camila/miniconda3/envs/amazon-storms-aerosols/bin/python

"""
Check if Level 2 (.nc) are created and tar.gz .mmclx and .znc files if so
@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import sys
import subprocess
import time
from pathlib import Path
from glob import glob


# Defining path of data files
data_path = "/home/camila/git/amazon-storms-aerosols/data/radar/mira_campina/"

# Listing .nc files
nc_files = sorted(glob(data_path + "*/*/*/*.nc", recursive=True))
print(nc_files)

# Listing .mmclx.tar.gz files
mmclx_files = sorted(glob(data_path + "*/*/*/*.mmclx.tar.gz", recursive=True))
print(mmclx_files)

# Matching .nc and .mmclx files
if len(mmclx_files) == 0:
    id = -1
else:
    id = nc_files.index(mmclx_files[-1][:-13] + ".nc")
print(id)
if id == len(nc_files):
    sys.exit("No new files")
else:
    mmclx_to_zip = nc_files[id + 1][:-3] + ".mmclx"
    print(mmclx_to_zip)
    znc_to_zip = nc_files[id + 1][:-3] + ".znc"

    # Converting .mmclx to .tar.gz
    bt = time.time()
    subprocess.call(
        [
            "/bin/tar",
            "-zcvf",
            mmclx_to_zip + ".tar.gz",
            mmclx_to_zip,
            "--remove-files",
        ]
    )
    print((time.time() - bt) / 60, "minutes to zip", mmclx_to_zip)

    # Converting .znc to .tar.gz if available
    try:
        bt = time.time()
        subprocess.call(
            [
                "/bin/tar",
                "-zcvf",
                znc_to_zip + ".tar.gz",
                znc_to_zip,
                "--remove-files",
            ]
        )
        print((time.time() - bt) / 60, "minutes to zip", znc_to_zip)
    except:
        pass


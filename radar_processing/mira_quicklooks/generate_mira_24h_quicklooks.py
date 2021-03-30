#!/home/cclopes/miniconda3/envs/amazon-storms-aerosols/bin/python

"""
Main script to generate 24h quicklooks of MIRA radar data

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import shutil
import os
import sys
import time
from pathlib import Path
from glob import glob
from zipfile import ZipFile

from plot_mira_quicklooks import read_plot_mira_quicklooks


def unzip_files(file, path):
    """
    Unzip a file.

    Parameters
    ----------
    file: name of zip file
    path: full path of folder with zip files

    Returns
    -------
    paths: list of unzipped files
    """

    bt = time.time()

    with ZipFile(file, "r") as zip_ref:
        zip_filenames = zip_ref.namelist()
        for filename in zip_filenames:
            if filename.endswith(".mmclx"):
                zip_ref.extract(filename, path + "temp/")

    paths = sorted(glob(path + "temp/" + file[-6:-4] + "/*"))

    print((time.time() - bt) / 60, " minutes to unzip files")

    return paths


# Defining path of data files
data_path = "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/data/radar/mira_campina/"

# Creating quicklooks folders (if it doesn't exist)
Path(data_path + "quicklooks").mkdir(parents=True, exist_ok=True)

# Checking quicklooks files (if exists)
if os.listdir(data_path + "quicklooks"):
    ql_folders = sorted(glob(data_path + "quicklooks/*/*/*/", recursive=True))
    ql_last = ql_folders[-1][-11:-1]
else:
    ql_last = ""

# Listing data files
data_files = sorted(glob(data_path + "*/*/*.zip", recursive=True))

# Selecting next date after the last one with quicklooks
# (or first if there's no quicklooks)
if data_path + ql_last + ".zip" in data_files:
    if (data_files.index(data_path + ql_last + ".zip") + 1) >= len(data_files):
        sys.exit("No new files")
    else:
        data_ql = data_files[data_files.index(data_path + ql_last + ".zip") + 1]
else:
    data_ql = data_files[0]

# Generating quicklooks of data_ql

# Unziping data
files = unzip_files(data_ql, data_path)
if len(files) <= 3:
    Path(data_path + "quicklooks/" + ql_last + "/").mkdir(
        parents=True, exist_ok=True
    )
    sys.exit("Not enough files to plot")

# Plotting
bt = time.time()
read_plot_mira_quicklooks(
    filenames=files, save_path=data_path + "quicklooks/", res=2
)
print((time.time() - bt) / 60, " minutes to generate quicklooks for")
print(data_ql)

# Deleting temporary files
shutil.rmtree(data_path + "temp/")

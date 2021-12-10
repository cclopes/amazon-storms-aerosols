#!/home/camila/miniconda3/envs/amazon-storms-aerosols/bin/python

"""
Main script to generate 24h quicklooks of MIRA radar data

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import sys
import time
from pathlib import Path
from glob import glob

from plot_mira_quicklooks import read_plot_mira_quicklooks


# Defining path of data files
data_path = "/home/camila/git/amazon-storms-aerosols/data/radar/mira_campina/"

# Checking quicklooks files (if exists)
ql_files = sorted(
    glob(
        data_path
        + "figs/Health/Mira35_Health_Campina_*_"
        + ("[0-9]" * 2)
        + "_*.png",
        recursive=True,
    )
)
if len(ql_files) == 0:
    ql_last = ""
else:
    ql_last = ql_files[-1]
    ql_last = ql_last[-14:-4].replace("_", "/")
# print(ql_last)

# Listing data files
data_files = sorted(glob(data_path + "20*/*/*/*.mmclx", recursive=True))
data_folders = sorted(list(set([i[-30:-20] for i in data_files])))
# print(data_folders)

# Selecting next date after the last one with quicklooks
# (or first if there's no quicklooks)
if ql_last in data_folders:
    if (data_folders.index(ql_last) + 1) >= len(data_folders):
        sys.exit("No new files")
    else:
        data_ql = data_folders[data_folders.index(ql_last) + 1]
else:
    data_ql = data_folders[1]
data_ql = "2021/11/09"
print(data_ql)

# Generating quicklooks of data_ql
files = sorted(glob(data_path + data_ql + "/*.mmclx", recursive=True))
# print(files)
if len(files) <= 3:
    Path(
        data_path
        + "figs/Health/Mira35_Health_Campina_"
        + str(data_ql.split("/")[0])
        + "_"
        + str(data_ql.split("/")[1])
        + "_"
        + str(data_ql.split("/")[2])
        + ".png"
    ).touch()
    Path(
        data_path
        + "figs/Reflectivity/Mira35_Reflectivity_Campina_"
        + str(data_ql.split("/")[0])
        + "_"
        + str(data_ql.split("/")[1])
        + "_"
        + str(data_ql.split("/")[2])
        + ".png"
    ).touch()
    Path(
        data_path
        + "figs/Vel_Doppler/Mira35_Vel_Doppler_Campina_"
        + str(data_ql.split("/")[0])
        + "_"
        + str(data_ql.split("/")[1])
        + "_"
        + str(data_ql.split("/")[2])
        + ".png"
    ).touch()
    Path(
        data_path
        + "figs/LDR/Mira35_LDR_Campina_"
        + str(data_ql.split("/")[0])
        + "_"
        + str(data_ql.split("/")[1])
        + "_"
        + str(data_ql.split("/")[2])
        + ".png"
    ).touch()
    sys.exit("Not enough files to plot - creating empty plot for " + data_ql)

# Plotting
bt = time.time()
read_plot_mira_quicklooks(
    filenames=files, save_path=data_path + "figs/", res=2,
)
print(
    (time.time() - bt) / 60,
    "minutes to generate quicklooks for",
    data_ql.replace("/", "-"),
)

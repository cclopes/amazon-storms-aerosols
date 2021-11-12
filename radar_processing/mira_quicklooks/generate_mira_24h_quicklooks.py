#!/home/camila/miniconda3/envs/amazon-storms-aerosols/bin/python

"""
Main script to generate 24h quicklooks of MIRA radar data

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import sys
import time
from glob import glob

from plot_mira_quicklooks import read_plot_mira_quicklooks


# Defining path of data files
data_path = "/home/camila/git/amazon-storms-aerosols/data/radar/mira_campina/"

# Checking quicklooks files (if exists)
ql_files = sorted(glob(data_path + "figs/*/*.png", recursive=True))
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
# print(data_ql)

# Generating quicklooks of data_ql
files = sorted(glob(data_path + data_ql + "/*.mmclx", recursive=True))
# print(files)
if len(files) <= 3:
    Path(data_path + "quicklooks/" + ql_last + "/").mkdir(
        parents=True, exist_ok=True
    )
    sys.exit("Not enough files to plot")

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

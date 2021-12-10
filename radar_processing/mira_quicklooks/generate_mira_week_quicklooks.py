#!/home/camila/miniconda3/envs/amazon-storms-aerosols/bin/python

"""
Main script to generate weekly quicklooks of MIRA radar data

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import sys
import time
import datetime
from glob import glob
from pathlib import Path

from plot_mira_quicklooks import read_plot_mira_quicklooks


# Defining path of data files
data_path = "/home/camila/git/amazon-storms-aerosols/data/radar/mira_campina/"

# Checking quicklooks files (if exists)
ql_files = sorted(
    glob(
        data_path + "figs/Health/Mira35_Health_Campina_*_week_*.png",
        recursive=True,
    )
)
if len(ql_files) == 0:
    ql_last = "none"
else:
    ql_last = datetime.datetime.strptime(
        ql_files[-1][-16:-4] + "_" + str(7), "%G_week_%V_%u"
    )
print(ql_last)

# Listing data files
data_files = sorted(glob(data_path + "20*/*/*/*.mmclx", recursive=True))
data_folders = sorted(list(set([i[-30:-20] for i in data_files])))
# print(data_folders)

# Selecting next week after the last one with quicklooks
# (or first if there's no quicklooks)
# and generating list of corresponding week
if ql_last == "none":
    data_week = data_folders[0].split("/")
    data_week = datetime.date(
        int(data_week[0]), int(data_week[1]), int(data_week[2])
    ).isocalendar()
    # print(data_week)
    data_ql = []
    for i in [1, 2, 3, 4, 5, 6, 7]:
        data_ql.append(
            datetime.datetime.strptime(
                str(data_week[0]) + " " + str(data_week[1]) + " " + str(i),
                "%G %V %u",
            ).strftime("%Y/%m/%d")
        )
else:
    data_week = ql_last + datetime.timedelta(days=1)
    data_week = data_week.isocalendar()
    data_ql = []
    for i in [1, 2, 3, 4, 5, 6, 7]:
        data_ql.append(
            datetime.datetime.strptime(
                str(data_week[0]) + " " + str(data_week[1]) + " " + str(i),
                "%G %V %u",
            ).strftime("%Y/%m/%d")
        )
print(data_ql)

# Generating quicklooks of data_ql
files = []
for day in data_ql:
    files.append(sorted(glob(data_path + day + "/*.mmclx", recursive=True)))
files = [item for sublist in files for item in sublist]
if len(files) < 12:
    Path(
        data_path
        + "figs/Health/Mira35_Health_Campina_"
        + str(data_week[0])
        + "_week_"
        + str(data_week[1])
        + ".png"
    ).touch()
    Path(
        data_path
        + "figs/Reflectivity/Mira35_Reflectivity_Campina_"
        + str(data_week[0])
        + "_week_"
        + str(data_week[1])
        + ".png"
    ).touch()
    Path(
        data_path
        + "figs/Vel_Doppler/Mira35_Vel_Doppler_Campina_"
        + str(data_week[0])
        + "_week_"
        + str(data_week[1])
        + ".png"
    ).touch()
    Path(
        data_path
        + "figs/LDR/Mira35_LDR_Campina_"
        + str(data_week[0])
        + "_week_"
        + str(data_week[1])
        + ".png"
    ).touch()
    sys.exit(
        "Not enough files - created empty plot for week "
        + str(
            datetime.datetime.strptime(data_ql[1], "%Y/%m/%d").isocalendar()[:2]
        )
    )
# print(files)

# Plotting
bt = time.time()
read_plot_mira_quicklooks(
    filenames=files, save_path=data_path + "figs/", res=30, is_weekly_fig=True,
)
print(
    (time.time() - bt) / 60,
    "minutes to generate quicklooks for week ",
    str(datetime.datetime.strptime(data_ql[1], "%Y/%m/%d").isocalendar()[:2]),
)

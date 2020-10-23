import time

from grab_mira_files import unzip_files
from plot_mira_quicklooks import read_plot_mira_quicklooks

# Count the time
bt = time.time()

files_month = unzip_files("data/radar/mira_campina/2020/06/")

for files_day in files_month:
    files_day.sort()
    files_0_7 = files_day[:8]
    files_8_15 = files_day[8:16]
    files_16_23 = files_day[16:]

    read_plot_mira_quicklooks(files_0_7, "radar_processing/figs/quicklooks/")

    read_plot_mira_quicklooks(files_8_15, "radar_processing/figs/quicklooks/")

    read_plot_mira_quicklooks(files_16_23, "radar_processing/figs/quicklooks/")

print(time.time() - bt, " seconds to run script")

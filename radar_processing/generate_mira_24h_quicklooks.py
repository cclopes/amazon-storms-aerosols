import time

from grab_mira_files import unzip_files
from plot_mira_quicklooks import read_plot_mira_quicklooks

# Count the time
bt = time.time()

files_day = unzip_files("data/radar/mira_campina/2020/03/06/")

read_plot_mira_quicklooks(
    files_day, "radar_processing/figs/quicklooks/", res=10
)

print((time.time() - bt) / 60, " minutes to generate quicklooks")

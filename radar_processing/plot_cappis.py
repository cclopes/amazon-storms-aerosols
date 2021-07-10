#%%
"""
Quick CAPPI plotting

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from glob import glob

from plot_functions import plot_basic_cappi


# Defining paths
path = "/home/cclopes/git/amazon-storms-aerosols/"
path_cappis = "data/radar/sipam_manaus/arm_cappi/2015-04/"
cappis = glob(path + path_cappis + "*/*")
rivers = "data/general/shapefiles/lineaire_1km"
cities = "data/general/shapefiles/AM_Municipios_2019"

# Plotting CAPPIs
for cappi in cappis:
    for level in range(4, 8):
        plot_basic_cappi(path, cappi, level, rivers, cities)

# %%

"""
Plotting PPIs and SIPAM Scan Strategy

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from glob import glob

from plot_functions import plot_basic_ppi, plot_scan_strategy

path = "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/"
path_ppis = "data/radar/sipam_manaus/arm/201401/"
ppis = glob(path + path_ppis + "*" + "RADL08061720140103031200.HDF5")
rivers = "data/general/shapefiles/lineaire_1km"
states = "data/general/shapefiles/ne_10m_admin_1_states_provinces"

# for ppi in ppis:
#     for level in range(13):
#         plot_basic_ppi(path, ppi, level, rivers, states)

plot_scan_strategy(path, ppis[0])

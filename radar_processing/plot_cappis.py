"""
Quick CAPPI plotting

@author: Camila Lopes (cclopes.me)
"""

from glob import glob

from plot_functions import plot_basic_cappi

# Defining paths
path = "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/"
path_cappis = "data/radar/sipam_manaus/arm_cappi/2014-03/20140303/"
cappis = glob(path + path_cappis + "*")
rivers = "data/general/shapefiles/lineaire_1km"
states = "data/general/shapefiles/ne_10m_admin_1_states_provinces"

for cappi in cappis:
    for level in range(11):
        plot_basic_cappi(path, cappi, level, rivers, states)

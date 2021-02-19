"""
Testing Stratiform/Convective classification

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from glob import glob

from matplotlib import pyplot as plt

import pyart

from read_sipam_cappis import read_sipam_cappi


# Getting radar files
path = "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/"
path_cappis = "data/radar/sipam_manaus/arm_cappi/"
cappis = glob(path_cappis + "2014-03/20140301/*")

# Reading file
cappi = read_sipam_cappi(cappis[43])
print(cappi.get_projparams())

# Calculando a classificação
strat_conv = pyart.retrieve.steiner_conv_strat(
    cappi, intense=40, refl_field="DBZc"
)

# Plotando
fig = plt.figure(figsize=(8, 7))
plt.pcolormesh(strat_conv["data"])
plt.colorbar()
plt.savefig("tracking/figs/test_strat_conv.png")
plt.close()

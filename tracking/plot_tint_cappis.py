"""
Testing basic TINT functionality

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from glob import glob

import numpy as np
import pickle

from matplotlib import pyplot as plt

from tint import animate
from tint.visualization import lagrangian_view, full_domain

from read_sipam_cappis import read_sipam_cappi


# Getting radar files
path = "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/"
path_cappis = "data/radar/sipam_manaus/arm_cappi/"
cappis = (
    glob(path + path_cappis + "2014-03/20140301/*")
    + glob(path + path_cappis + "2014-03/20140302/*")
    + glob(path + path_cappis + "2014-03/20140303/*")
)
print("number of radar files: " + str(len(cappis)))

# Shapefile path
rivers = "data/general/shapefiles/lineaire_1km"
states = "data/general/shapefiles/ne_10m_admin_1_states_provinces"

# -- Loading results from pickle
with open("tracking/tracks_obj.pkl", "rb") as data:
    tracks_obj = pickle.load(data)
print(tracks_obj.tracks.head(10))

# - Plotting results
grids = (read_sipam_cappi(cappi) for cappi in cappis)
full_domain(
    tracks_obj,
    grids,
    path + "tracking/figs/test/full_domain_20dbz",
    vmin=0,
    vmax=70,
    alt=3000,
    lon_lines=np.arange(-62.5, -56.5, 1),
    lat_lines=np.arange(-5.5, 0.5, 1),
    tracers=True,
)
# -- Save in .mp4
animate(
    tracks_obj,
    grids,
    path + "tracking/figs/tracking_anim",
    vmin=10,
    vmax=70,
    fps=2,
    alt=3000,
    lon_lines=np.arange(-62.5, -56.5, 1),
    lat_lines=np.arange(-5.5, 0.5, 1),
    tracers=True,
)

# - Longer cells
print(
    tracks_obj.tracks.groupby(level="uid")
    .size()
    .sort_values(ascending=False)[:10]
)
print(tracks_obj.tracks.groupby("uid").max())

# - Histograms
distr = tracks_obj.tracks.groupby(level="uid").size() * 12
distr.plot.hist(bins=26)
plt.xlabel("Time (min)")
plt.savefig("tracking/figs/histogram.png", dpi=300)

distr = tracks_obj.tracks.groupby(level="uid").max()
distr["max"].plot.hist()
plt.xlabel("Max Reflectivity (dBZ)")
plt.savefig("tracking/figs/histogram_maxz.png", dpi=300)

distr = tracks_obj.tracks.groupby(level="uid").max()
distr["area"].plot.hist()
plt.xlabel("Max Area (km²)")
plt.savefig("tracking/figs/histogram_maxarea.png", dpi=300)

distr = tracks_obj.tracks.groupby(level="uid").max()
distr["vol"].plot.hist()
plt.xlabel("Max Volume (km³)")
plt.savefig("tracking/figs/histogram_maxvol.png", dpi=300)

# - Lagrangian view of one of the cells
grids = (read_sipam_cappi(cappi) for cappi in cappis)
lagrangian_view(
    tracks_obj,
    grids,
    path + "tracking/figs/test/lagrangian_cell456_20dbz",
    uid="456",
    vmin=0,
    vmax=70,
    cmap="dbz",
    alt=3000,
)
# -- Save in .mp4
animate(
    tracks_obj,
    grids,
    path + "tracking/figs/lagrangian_anim_cell88_32dbz",
    style="lagrangian",
    uid="88",
    alt=2000,
    vmin=10,
    vmax=70,
)

"""
Testing basic TINT functionality

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from glob import glob
import tempfile
import os
import time
import tarfile
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pickle

import netCDF4

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import pyart
from tint import Cell_tracks, animate
from tint.visualization import lagrangian_view, full_domain

import custom_cbars
from read_sipam_cappis import read_sipam_cappi


# Getting radar files
path = (
    "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/"
)
path_cappis = "data/radar/sipam_manaus/arm_cappi/"
cappis = glob(path + path_cappis + "20140103/*") + glob(
    path + path_cappis + "20140104/*"
)
print("number of radar files: " + str(len(cappis)))

rivers = "data/general/shapefiles/lineaire_1km"
states = "data/general/shapefiles/ne_10m_admin_1_states_provinces"

# Testing stratiform/convective classification
# cappi = read_sipam_cappi(cappis[92])
# print(cappi.get_projparams())
# grid = pyart.io.read_grid('data/radar/sipam_manaus/arm/201401/RADL08061720140103132400_grid.nc')
# print(grid.get_projparams())
# strat_conv = pyart.retrieve.steiner_conv_strat(cappi, intense=40,
#     refl_field='DBZc')
# fig = plt.figure(figsize=(8, 7))
# plt.pcolormesh(strat_conv['data'])
# plt.colorbar()
# plt.savefig('tracking/figs/test_strat_conv.png')
# plt.close()

# Separating according to data availability (IF NECESSARY)
# p = 1
# files['period'] = 'p' + str(p)
# delta = datetime.strptime("01:00:00", "%H:%M:%S")
# delta = timedelta(hours=delta.hour, minutes=delta.minute, seconds=delta.second)

# for i in np.arange(1,len(files['date'])):
#     if (files['date'][i] - files['date'][i-1]) < delta:
#         files['period'] = 'p' + str(p)
#     else:
#         p = p + 1
#         files['period'] = 'p' + str(p)


# TESTING
# - Separating test period
subfiles = cappis[49:110]
# grids = (read_sipam_cappi(file) for file in subfiles)

# - Tracking
tracks_obj = Cell_tracks(field="DBZc")
tracks_obj.params["FIELD_THRESH"] = 20
tracks_obj.params["MIN_SIZE"] = 10
print(tracks_obj.params)

# tracks_obj.get_tracks(grids)
# # print(tracks_obj.tracks.head(10))

# -- Saving results temporarily
# with open('tracking/tracks_obj.pkl', 'wb') as output:
#     pickle.dump(tracks_obj, output)

# -- Loading results from pickle
# with open('tracking/tracks_obj.pkl', 'rb') as data:
#     tracks_obj = pickle.load(data)
# print(tracks_obj.tracks.head(10))

# - Plotting results
# grids = (read_sipam_cappi(file) for file in subfiles)
# full_domain(
#     tracks_obj, grids, path + 'tracking/figs/test/full_domain_20dbz',
#     vmin=0, vmax=70, alt=3000,
#     lon_lines=np.arange(-62.5, -56.5, 1), lat_lines=np.arange(-5.5, 0.5, 1),
#     tracers=True
# )
# -- Save in .mp4
# animate(
#     tracks_obj, grids, path + 'tracking/figs/tracking_anim',
#     vmin=10, vmax=70, fps=2, alt=3000,
#     lon_lines=np.arange(-62.5, -56.5, 1), lat_lines=np.arange(-5.5, 0.5, 1),
#     tracers=True
# )

# - Longer cells
# print(tracks_obj.tracks.groupby(level='uid').size().sort_values(ascending=False)[:10])
# print(tracks_obj.tracks.groupby('uid').max())
# distr = tracks_obj.tracks.groupby(level='uid').size()*12
# distr.plot.hist(bins=26)
# plt.xlabel('Time (min)')
# plt.savefig('tracking/figs/histogram.png', dpi=300)
# distr = tracks_obj.tracks.groupby(level='uid').max()
# distr['max'].plot.hist()
# plt.xlabel('Max Reflectivity (dBZ)')
# plt.savefig('tracking/figs/histogram_maxz.png', dpi=300)
# distr = tracks_obj.tracks.groupby(level='uid').max()
# distr['area'].plot.hist()
# plt.xlabel('Max Area (km²)')
# plt.savefig('tracking/figs/histogram_maxarea.png', dpi=300)
# distr = tracks_obj.tracks.groupby(level='uid').max()
# distr['vol'].plot.hist()
# plt.xlabel('Max Volume (km³)')
# plt.savefig('tracking/figs/histogram_maxvol.png', dpi=300)

# - Lagrangian view of one of the cells
# grids = (read_sipam_cappi(file) for file in subfiles)
# lagrangian_view(
#     tracks_obj, grids, path + 'tracking/figs/test/lagrangian_cell456_20dbz',
#     uid='456', vmin=0, vmax=70, cmap='dbz', alt=3000
# )
# -- Save in .mp4
# animate(
#     tracks_obj, grids, path + 'tracking/figs/lagrangian_anim_cell88_32dbz',
#     style='lagrangian', uid='88', alt=2000, vmin=10, vmax=70
# )

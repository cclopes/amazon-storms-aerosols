"""
Testing basic TINT functionality

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

#%%
import glob
import tempfile
import os
import time
import tarfile
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import netCDF4

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, Image, display
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import pyart
from tint import Cell_tracks, animate
from tint.visualization import lagrangian_view, full_domain

import custom_cbars
from plot_functions import plot_basic_ppi

def ppi_to_grid(filename):
    
    # Count the time
    bt = time.time()

    # Read data and convert to grid
    radar = pyart.aux_io.read_gamic(filename)
    grid = pyart.map.grid_from_radars(
        radar, grid_shape=(20, 501, 501),
        grid_limits=((1e3, 20e3), (-250e3, 250e3), (-250e3, 250e3))
    )

    # Save grid to file
    pyart.io.write_grid(filename[:-5] + '_grid.nc', grid)

    print(time.time()-bt, ' seconds to grid radar')

    return grid


#%%
# Getting radar files
path = '/home/camila/git/amazon-storms-aerosols/'
file_level = 'level_2/'
file_ext = '.nc'

filenames = glob.glob(
    path + 'data/radar/sipam_manaus/arm/' + file_level + '**/*' + file_ext,
     recursive=True)
print("number of radar files: " + str(len(filenames)))

files = pd.DataFrame(filenames, columns=['filename'])
files['date'] = pd.to_datetime(
    files['filename'].str.extract('RADL080617(\d{14})')[0], 
    format='%Y%m%d%H%M%S'
    )
files['filegrids'] = files['filename'].str.replace(file_ext, '_grid.nc')
files = files.sort_values('date').reset_index(drop=True)
del filenames

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

#%%
# Generating png figures and zipping them
files = files.iloc[18:20]
for file, date in zip(files.filename, files.date):
    fig = plt.figure(figsize=(8, 7))
    plot_basic_ppi(file, date)
# with tarfile.open(path + 'tracking/figs/Z_0_9.tar.gz', 'w:gz') as tar:
#     tar.add(path + 'tracking/figs', arcname='.')
# Generating gif of all files
# fig = plt.figure(figsize=(8, 7))
# ppi_anim = FuncAnimation(
#     fig, plot_basic_ppi, frames=files['filename'][3066:], interval=500)
# ppi_anim.save(path + 'tracking/test_sep2014.gif', writer='imagemagick')

# TESTING
#%%
# - Separating test period
# subfiles = files.iloc[51:107]

#%%
# - Converting to grids

# -- quick test
# test = ppi_to_grid(subfiles['filename'][3130])
# fig = plt.figure()
# display = pyart.graph.GridMapDisplay(test)
# display.plot_grid('corrected_reflectivity', 1, vmin=10, vmax=70)

# - Writing grids (run only once!)
# grids = [ppi_to_grid(f) for f in subfiles['filename']]

#%%
# - Tracking
# tracks_obj = Cell_tracks(field='corrected_reflectivity')
# print(tracks_obj.params)

# -- Reading generated grids (faster than converting/tracking)
# grids = (pyart.io.read_grid(f) for f in subfiles['filegrids'])
# tracks_obj.get_tracks(grids)
# -- Results
# tracks_obj.tracks.head(10)

#%%
# - Plotting results
# grids = (pyart.io.read_grid(f) for f in subfiles['filegrids'])
# full_domain(
#     tracks_obj, grids, path + 'tracking/figs/test/full_domain_32dbz',
#     vmin=0, vmax=70, 
#     lon_lines=np.arange(-62.5, -56.5, 1), lat_lines=np.arange(-5.5, 0.5, 1),
#     tracers=True
# )
# -- Save in .mp4
# animate(
#     tracks_obj, grids, path + 'tracking/figs/tracking_anim',
#     vmin=10, vmax=70, fps=2, 
#     lon_lines=np.arange(-62.5, -56.5, 1), lat_lines=np.arange(-5.5, 0.5, 1),
#     tracers=True
# )
#%%
# - Longer cells
# tracks_obj.tracks.groupby(level='uid').size().sort_values(ascending=False)[:5]
#%%
# - Lagrangian view of one of the cells
# grids = (pyart.io.read_grid(f) for f in subfiles['filegrids'])
# lagrangian_view(
#     tracks_obj, grids, path + 'tracking/figs/test/lagrangian_cell88_32dbz',
#     uid='88', vmin=0, vmax=70, cmap='dbz', alt=1000
# )
# -- Save in .mp4
# animate(
#     tracks_obj, grids, path + 'tracking/figs/lagrangian_anim_cell88_32dbz',
#     style='lagrangian', uid='88', alt=2000, vmin=10, vmax=70
# )



# %%

"""
Testing basic TINT functionality

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from glob import glob

import pickle

from tint import Cell_tracks

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

# TESTING
# Reading files
grids = (read_sipam_cappi(cappi) for cappi in cappis)

# - Tracking
tracks_obj = Cell_tracks(field="DBZc")
tracks_obj.params["FIELD_THRESH"] = 20
tracks_obj.params["MIN_SIZE"] = 10
print(tracks_obj.params)

tracks_obj.get_tracks(grids)
print(tracks_obj.tracks.head(10))

# -- Saving results temporarily
with open("tracking/tracks_obj.pkl", "wb") as output:
    pickle.dump(tracks_obj, output)

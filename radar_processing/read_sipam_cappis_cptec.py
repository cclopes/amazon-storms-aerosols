"""
Reading SIPAM CAPPI objects generated by DSA/CPTEC-INPE.

Data source:
http://ftp.cptec.inpe.br/chuva/goamazon/experimental/level_2/eq_radar/esp_band_s/st_sipam/

Adapted from pyart.io.read_grid source code
(https://arm-doe.github.io/pyart/_modules/pyart/io/grid_io.html)

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

from datetime import datetime
import re

import numpy as np

from pyart.core.grid import Grid


def read_simple_cappi(filename, latlon_path):
    """Reading binary CAPPI grids produced by CPTEC to array"""

    # Reading data
    cappis = np.fromfile(filename, dtype="float32").reshape(15, 500, 500)[:, ::2, ::2]

    # Reading lat/lon files
    lon_grid = np.fromfile(latlon_path + "/lon_SBMN_500.txt", sep="   ").reshape(
        500, 500
    )[::2, ::2]
    lat_grid = np.fromfile(latlon_path + "/lat_SBMN_500.txt", sep="   ").reshape(
        500, 500
    )[::2, ::2]
    return cappis, [lon_grid, lat_grid]


def read_sipam_cappi(
    filename,
    exclude_fields=[
        "start_time",
        "stop_time",
        "time_bounds",
        "x0",
        "y0",
        "lat0",
        "lon0",
        "z0",
        "grid_mapping_0",
    ],
    include_fields=None,
    **kwargs
):
    """
    Read a netCDF grid file produced by Py-ART.

    Parameters
    ----------
    filename : str
        Filename of netCDF grid file to read. This file must have been
        produced by :py:func:`write_grid` or have identical layout.

    Other Parameters
    ----------------
    exclude_fields : list or None, optional
        List of fields to exclude from the radar object. This is applied
        after the `file_field_names` and `field_names` parameters. Set
        to None to include all fields specified by include_fields.
    include_fields : list or None, optional
        List of fields to include from the radar object. This is applied
        after the `file_field_names` and `field_names` parameters. Set
        to None to include all fields not specified by exclude_fields.

    Returns
    -------
    grid : Grid
        Grid object containing gridded data.

    """
    # test for non empty kwargs
    # _test_arguments(kwargs)

    if exclude_fields is None:
        exclude_fields = []

    reserved_variables = [
        "time",
        "x",
        "y",
        "z",
        "origin_latitude",
        "origin_longitude",
        "origin_altitude",
        "point_x",
        "point_y",
        "point_z",
        "projection",
        "point_latitude",
        "point_longitude",
        "point_altitude",
        "radar_latitude",
        "radar_longitude",
        "radar_altitude",
        "radar_name",
        "radar_time",
        "base_time",
        "time_offset",
        "ProjectionCoordinateSystem",
    ]

    # dset = netCDF4.Dataset(filename, mode="r")
    dset = np.fromfile(filename, dtype="float32").reshape(15, 500, 500)[:, ::2, ::2]
    # dset[dset == -99.] = np.nan

    # metadata
    metadata = {
        "institution": "DSA/CPTEC-INPE",
        "source": "http://ftp.cptec.inpe.br/chuva/goamazon/experimental/level_2/eq_radar/esp_band_s/st_sipam/",
    }

    # required reserved variables
    file_time = datetime.strptime(re.findall(r"\d{12}", filename)[0], "%Y%m%d%H%M%S")
    time = {
        "units": "seconds since 1970-01-01T00:00:00Z",
        "data": [file_time.timestamp()],
    }
    origin_latitude = {
        "data": [-3.1493],
        "long_name": "Latitude of projection origin",
        "units": "degree_N",
    }
    origin_longitude = {
        "data": [-59.9920],
        "long_name": "Longitude of projection origin",
        "units": "degree_E",
    }
    origin_altitude = None
    x = {"data": np.arange(-250000, 250000, 2000), "units": "m"}
    y = {"data": np.arange(-250000, 250000, 2000), "units": "m"}
    z = {"data": np.arange(2000, 17000, 1000), "units": "m"}

    # projection
    projection = {"data": [], "proj": "aeqd", "_include_lon_0_lat_0": "true"}
    projection.pop("data")
    # map _include_lon_0_lat_0 key to bool type
    if "_include_lon_0_lat_0" in projection:
        v = projection["_include_lon_0_lat_0"]
        projection["_include_lon_0_lat_0"] = {"true": True, "false": False}[v]

    # read in the fields
    fields = {
        "corrected_reflectivity": {
            "_FillValue": -99.0,
            "standard_name": "Corrected Reflectivity",
            "long_name": "Corrected Reflectivity",
            "units": "dBZ",
            "data": dset,
        }
    }

    # radar_ variables
    radar_latitude = {
        "long_name": "Latitude of radars used to make the grid.",
        "units": "degrees_north",
        "data": np.array([-3.1493]),
    }
    radar_longitude = {
        "long_name": "Longitude of radars used to make the grid.",
        "units": "degrees_east",
        "data": np.array([-59.992]),
    }
    radar_altitude = {
        "long_name": "Altitude of radars used to make the grid.",
        "units": "m",
        "data": np.array([102.4]),
    }
    radar_name = {
        "long_name": "Name of radar used to make the grid",
        "data": np.array(["SIPAM"], dtype="<U1"),
    }

    radar_time = None

    return Grid(
        time,
        fields,
        metadata,
        origin_latitude,
        origin_longitude,
        origin_altitude,
        x,
        y,
        z,
        projection=projection,
        radar_latitude=radar_latitude,
        radar_longitude=radar_longitude,
        radar_altitude=radar_altitude,
        radar_name=radar_name,
        radar_time=radar_time,
    )

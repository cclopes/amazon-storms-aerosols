"""
Plotting functions for radar data

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import os
import gc
import numpy as np
from matplotlib import pyplot as plt

import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pyart
import wradlib as wrl

import custom_cbars
from read_sipam_cappis import read_sipam_cappi


def plot_basic_ppi(path, filename, level, shape_rivers, shape_states):
    """
    Plot "corrected_reflectivity" field in a level.

    Parameters
    ----------
    path: full path of repository
    filename: path + name of GAMIC-compatible radar file
    level: level of PPI to plot
    shape_rivers: shapefile path of rivers
    shape_states: shapefile path of BR states
    """

    # Reading file and generating str for date and level
    radar = pyart.aux_io.read_gamic(filename)
    date = pyart.util.datetime_from_grid(radar)
    str_level = str("%.1f" % radar.fixed_angle["data"][level])

    # Creating directory to save figs
    save_path = (
        path
        + "radar_processing/figs/sipam_ppi/"
        + date.strftime("%Y-%m")
        + "/"
        + str_level
        + "/"
    )
    try:
        os.makedirs(save_path)
    except FileExistsError:
        pass

    # Plotting field
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    display = pyart.graph.RadarMapDisplay(radar)
    display.plot_ppi_map(
        "corrected_reflectivity",
        sweep=level,
        vmin=0,
        vmax=70,
        ax=ax,
        cmap="dbz",
        shapefile=path + shape_rivers,
        shapefile_kwargs={
            "facecolor": "None",
            "edgecolor": "darkblue",
            "alpha": 0.3,
            "linewidth": 0.75,
        },
    )
    # Adding shapefile
    ax.add_geometries(
        Reader(path + shape_states).geometries(),
        ccrs.PlateCarree(),
        linewidth=0.75,
        facecolor="None",
        edgecolor="gray",
        alpha=0.8,
    )
    # Adding gridlines
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        xlocs=np.arange(-70, -50, 1),
        ylocs=np.arange(-10, 1, 1),
    )
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    display.plot_range_rings(
        [50, 100, 150, 200, 250], ax=ax, col="lightgray", lw=1
    )

    # Saving figure
    plt.savefig(
        save_path
        + "sipam_"
        + str_level
        + "_dBZ_"
        + date.strftime("%Y%m%d%H%M%S")
        + ".png",
        bbox_inches="tight",
        dpi=300,
        facecolor="None",
        edgecolor="white",
    )
    plt.close()

    print("Plotted! " + str(date) + " - " + str_level + "°")


def plot_basic_cappi(path, filename, level, shape_rivers, shape_states):
    """
    Plot "DBZc" field in a level.

    Parameters
    ----------
    path: full path of repository
    filename: path + name of SIPAM CAPPI radar file
    level: level of CAPPI to plot
    shape_rivers: shapefile path of rivers
    shape_states: shapefile path of BR states
    """

    # Reading file and generating str for date and level
    radar = read_sipam_cappi(filename)
    date = pyart.util.datetime_from_grid(radar)
    str_level = str(radar.z["data"][level] / 1000)

    # Creating directory to save figs
    save_path = (
        path
        + "radar_processing/figs/sipam_cappi/"
        + date.strftime("%Y-%m")
        + "/"
        + str_level
        + "/"
    )
    try:
        os.makedirs(save_path)
    except FileExistsError:
        pass

    # Plotting field
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    display = pyart.graph.GridMapDisplay(radar)
    display.plot_grid(
        "DBZc", level=level, vmin=0, vmax=70, ax=ax, cmap="dbz", embelish=False
    )
    # Adding rivers
    ax.add_geometries(
        Reader(path + shape_rivers).geometries(),
        ccrs.PlateCarree(),
        linewidth=0.75,
        facecolor="None",
        edgecolor="darkblue",
        alpha=0.5,
    )
    # Adding shapefile
    ax.add_geometries(
        Reader(path + shape_states).geometries(),
        ccrs.PlateCarree(),
        linewidth=0.75,
        facecolor="None",
        edgecolor="darkgray",
        alpha=0.8,
    )
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        xlocs=np.arange(-70, -50, 1),
        ylocs=np.arange(-10, 1, 1),
        alpha=0.5,
    )
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # Saving figure
    plt.savefig(
        save_path
        + "sipam_"
        + str_level
        + "_dBZ_"
        + date.strftime("%Y%m%d%H%M%S")
        + ".png",
        bbox_inches="tight",
        dpi=300,
        facecolor="None",
        edgecolor="white",
    )
    plt.close()

    del radar, fig, ax, display, gl
    gc.collect()

    print("Plotted! " + str(date) + " - " + str_level + " km")


def plot_scan_strategy(path, filename):
    """
    Plot radar scan strategy.

    Parameters
    ----------
    path: full path of repository
    filename: path + name of GAMIC-compatible radar file
    """

    # Reading file, defining vars
    radar = pyart.aux_io.read_gamic(filename)
    ranges = radar.range["data"]
    elevs = radar.fixed_angle["data"]
    site = (
        float(radar.longitude["data"]),
        float(radar.latitude["data"]),
        float(radar.altitude["data"]),
    )
    beamwidth = float(radar.instrument_parameters["radar_beam_width_h"]["data"])

    # Plotting
    ax = wrl.vis.plot_scan_strategy(
        ranges, elevs, site, beamwidth, vert_res=1000, maxalt=20000, units="km"
    )
    ax.set_title("SIPAM S-Band")

    # Saving figure
    plt.savefig(
        path + "radar_processing/figs/sipam_scan_strategy.png",
        bbox_inches="tight",
        dpi=300,
        facecolor="None",
        edgecolor="white",
    )
    plt.close()

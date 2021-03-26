import time
import os
import gc
import shutil
from glob import glob
from zipfile import ZipFile
import matplotlib.pyplot as plt

import pyart

from read_mira_radar import read_mira


def unzip_files(file, path):
    """
    Unzip a file.

    Parameters
    ----------
    file: name of zip file
    path: full path of folder with zip files

    Returns
    -------
    paths: list of unzipped files
    """

    bt = time.time()

    with ZipFile(file, "r") as zip_ref:
        zip_filenames = zip_ref.namelist()
        for filename in zip_filenames:
            if filename.endswith(".mmclx"):
                zip_ref.extract(filename, path + "temp/")

    paths = glob(path + "temp/" + file[-6:-4] + "/*")

    print((time.time() - bt) / 60, " minutes to unzip files")

    return paths


def read_plot_mira(filenames, save_path="radar_processing/figs/mira/"):
    """
    Read and plot several fields of MIRA files.
    Fields plotted: "SNRg", "SNR", "Zg", "Ze", "VELg", "VEL", "LDRg", "LDR", 
        "RHO", "RHOwav", "DPS", "DPSwav", "RMSg", "RMS"

    Parameters
    ----------
    filenames: name of MIRA files
    save_path: path to save figures
    """

    # Reading files
    print("Reading MIRA files")
    mira, mira_melthei = read_mira(filenames, for_quicklooks=False)

    # Grabbing date from MIRA file
    # date = pyart.util.datetimes_from_radar(mira)[0]
    date = filenames[-19:-6]

    # Generating x axes for Melting Layer Height data
    # print(mira_melthei[0]['data'])
    # times = pyart.util.datetimes_from_radar(mira)
    # times = times.astype("datetime64[ns]")
    times = []

    # Plotando
    print("Plotting/saving MIRA variables")

    display = pyart.graph.RadarDisplay(mira)

    plot_mira_field(
        field="SNRg",
        times=times,
        melting_height=mira_melthei[0]["data"] / 1000,
        display=display,
        vmin=mira.fields["SNRg"]["yrange"][0],
        vmax=mira.fields["SNRg"]["yrange"][1],
        cmap="pyart_Carbone17",
        figname=save_path + "mira_snrg_" + date,  # .strftime("%Y%m%d%H%M%S")
    )

    # plot_mira_field(
    #     field="SNR",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["SNR"]["yrange"][0],
    #     vmax=mira.fields["SNR"]["yrange"][1],
    #     cmap="pyart_Carbone17",
    #     figname=save_path + "mira_snr_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="Zg",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["Zg"]["yrange"][0],
    #     vmax=40,
    #     cmap="pyart_Theodore16",
    #     figname=save_path + "mira_zg_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="Ze",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["Ze"]["yrange"][0],
    #     vmax=40,
    #     cmap="pyart_Theodore16",
    #     figname=save_path + "mira_ze_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="VELg",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["VELg"]["yrange"][0],
    #     vmax=mira.fields["VELg"]["yrange"][1],
    #     cmap="pyart_BuDRd18",
    #     figname=save_path + "mira_velg_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="VEL",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["VEL"]["yrange"][0],
    #     vmax=mira.fields["VEL"]["yrange"][1],
    #     cmap="pyart_BuDRd18",
    #     figname=save_path + "mira_vel_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="LDRg",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["LDRg"]["yrange"][0],
    #     vmax=mira.fields["LDRg"]["yrange"][1],
    #     cmap="pyart_SCook18",
    #     figname=save_path + "mira_ldrg_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="LDR",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["LDR"]["yrange"][0],
    #     vmax=mira.fields["LDR"]["yrange"][1],
    #     cmap="pyart_SCook18",
    #     figname=save_path + "mira_ldr_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="RHO",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["RHO"]["yrange"][0],
    #     vmax=mira.fields["RHO"]["yrange"][1],
    #     cmap="pyart_RefDiff",
    #     figname=save_path + "mira_rho_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="RHOwav",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["RHOwav"]["yrange"][0],
    #     vmax=mira.fields["RHOwav"]["yrange"][1],
    #     cmap="pyart_RefDiff",
    #     figname=save_path + "mira_rhowav_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="DPS",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["DPS"]["yrange"][0],
    #     vmax=mira.fields["DPS"]["yrange"][1],
    #     cmap="pyart_Wild25",
    #     figname=save_path + "mira_dps_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="DPSwav",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["DPSwav"]["yrange"][0],
    #     vmax=mira.fields["DPSwav"]["yrange"][1],
    #     cmap="pyart_Wild25",
    #     figname=save_path + "mira_dpswav_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="RMSg",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["RMSg"]["yrange"][0],
    #     vmax=mira.fields["RMSg"]["yrange"][1],
    #     cmap="pyart_NWS_SPW",
    #     figname=save_path + "mira_rmsg_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    # plot_mira_field(
    #     field="RMS",
    #     times=times,
    #     melting_height=mira_melthei[0]["data"] / 1000,
    #     display=display,
    #     vmin=mira.fields["RMS"]["yrange"][0],
    #     vmax=mira.fields["RMS"]["yrange"][1],
    #     cmap="pyart_NWS_SPW",
    #     figname=save_path + "mira_rms_" + date.strftime("%Y%m%d%H%M%S"),
    # )

    del mira, mira_melthei, date, times, display
    gc.collect()


def plot_mira_field(
    field, times, melting_height, display, vmin, vmax, cmap, figname
):
    """
    Plot a certain MIRA field.

    Parameters
    ----------
    field: name of field to be plotted
    times: list of timestamps for melting layer height plot
    melting_height: list of melting layer height data
    display: pyart.graph.RadarDisplay of MIRA radar data
    vmin: field min value
    vmax: field max value
    cmap: name of colormap to be used
    figname: path + figure name
    """

    plt.ioff()

    fig = plt.figure(figsize=(10, 5))  # (10, 5)

    display.plot_vpt(
        field,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        time_axis_flag=True,
        mask_outside=True,
        raster=True,
    )
    # plt.plot(times, melting_height, "k-", label="Melting Layer Height")
    display.plot_grid_lines()
    # plt.legend(loc="upper right")
    plt.ylim((0, 18))

    plt.savefig(figname + ".png", dpi=300, bbox_inches="tight")

    plt.clf()
    plt.close()
    del fig
    gc.collect()


# Defining filepath
data_path = (
    "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/"
    + "GitHub/amazon-storms-aerosols/data/radar/mira_campina/"
)

# Unzipping files
# files = unzip_files(data_path + "2020/10/31.zip", data_path)
# files = files[0]

# Plotting files
files = glob(data_path + "temp/*.mmclx")
for file in files:
    bt = time.time()
    read_plot_mira(filenames=file)
    print((time.time() - bt) / 60, " minutes to generate plot")

# shutil.rmtree(data_path + "temp/")

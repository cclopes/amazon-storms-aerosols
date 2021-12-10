"""
Plotting MIRA quicklooks

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import os
import gc
from datetime import datetime
import matplotlib.pyplot as plt
import pyart

from read_mira_radar import read_multi_mira


def read_plot_mira_quicklooks(
    filenames, save_path="figs/", res=5, is_weekly_fig=False
):
    """
    Read and plot several fields of MIRA files for 24h quicklooks.
    Fields plotted: "SNRg", "Ze", "VEL", "LDRg"

    Parameters
    ----------
    filenames: name of MIRA files
    save_path: path to save figures
    res: resolution (in minutes) of reprocessed data
    is_weekly_figs: flag for weekly figure
    """

    # Reading files
    print("Reading MIRA files")
    mira, mira_melthei, mira_mrm = read_multi_mira(
        filenames, for_quicklooks=True, ql_res=res
    )

    # Generating x axes for noise power plot
    times = pyart.util.datetimes_from_radar(mira)
    # Grabbing date from MIRA file
    date = times[0]
    # Generating date for title and fig name
    if is_weekly_fig:
        date_str = (
            times[len(times) % 2]._to_real_datetime().date().isocalendar()
        )
        if len(str(date_str[1])) == 1:
            date_str = list(date_str)
            date_str[1] = "0" + str(date_str[1])
            date_str = tuple(date_str)
        date_str = str(date_str[0]) + " week " + str(date_str[1])
        date_figname = date_str.replace(" ", "_")
    else:
        date_str = str(date)[:10]
        date_figname = date_str.replace("-", "_")

    # Plotting
    print("Plotting/saving MIRA fields")

    display = pyart.graph.RadarDisplay(mira)

    plot_mira_field(
        field="SNRg",
        display=display,
        vmin=mira.fields["SNRg"]["yrange"][0],
        vmax=mira.fields["SNRg"]["yrange"][1],
        cmap="pyart_Carbone17",
        title="Health status - " + date_str,
        times=times,
        mrm=mira_mrm["data"] * 1e1,
        figname=save_path + "Health/Mira35_Health_Campina_" + date_figname,
        is_weekly_fig=is_weekly_fig,
        health_fig=True,
    )

    plot_mira_field(
        field="Ze",
        display=display,
        vmin=mira.fields["Ze"]["yrange"][0],
        vmax=mira.fields["Ze"]["yrange"][1],
        cmap="pyart_Carbone17",
        title="Reflectivity (filtered) - " + date_str,
        times=times,
        mrm=mira_mrm["data"] * 1e1,
        figname=save_path
        + "Reflectivity/Mira35_Reflectivity_Campina_"
        + date_figname,
        is_weekly_fig=is_weekly_fig,
        health_fig=False,
    )

    plot_mira_field(
        field="VEL",
        display=display,
        vmin=mira.fields["VEL"]["yrange"][0],
        vmax=mira.fields["VEL"]["yrange"][1],
        cmap="pyart_BuDRd18",
        title="Doppler Velocity (filtered) - " + date_str,
        times=times,
        mrm=mira_mrm["data"] * 1e1,
        figname=save_path
        + "Vel_Doppler/Mira35_Vel_Doppler_Campina_"
        + date_figname,
        is_weekly_fig=is_weekly_fig,
        health_fig=False,
    )

    plot_mira_field(
        field="LDRg",
        display=display,
        vmin=mira.fields["LDRg"]["yrange"][0],
        vmax=mira.fields["LDRg"]["yrange"][1],
        cmap="pyart_SCook18",
        title="Linear De-Polarization Ratio (unfiltered) - " + date_str,
        times=times,
        mrm=mira_mrm["data"] * 1e1,
        figname=save_path + "LDR/Mira35_LDR_Campina_" + date_figname,
        is_weekly_fig=is_weekly_fig,
        health_fig=False,
    )

    del mira, mira_melthei, mira_mrm, times, display
    gc.collect()


def plot_mira_field(
    field,
    display,
    vmin,
    vmax,
    cmap,
    title,
    times,
    mrm,
    figname,
    is_weekly_fig=False,
    health_fig=False,
):
    """
    Plot a certain MIRA field.

    Parameters
    ----------
    field: name of field to be plotted
    melting_height: list of melting layer height data
    display: pyart.graph.RadarDisplay of MIRA radar data
    vmin: field min value
    vmax: field max value
    cmap: name of colormap to be used
    title: title of the plot
    times: list of timestamps for noise power plot
    mrm: noise power data to plot
    figname: path + figure name
    is_weekly_fig: flag for weekly figure
    health_fig: flag for health figure plot
    """

    plt.ioff()

    # Changing date label according to type of quicklook
    if is_weekly_fig:
        date_format = "%Y-%m-%d\n%H:%M"
        date_label = "Date"
    else:
        date_format = "%H:%M"
        date_label = "Time (HH:MM)"

    # Opening fig()
    fig = plt.figure(figsize=(15, 5))  # (10, 5)

    # Plotting
    display.plot_vpt(
        field,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        title=title,
        time_axis_flag=True,
        date_time_form=date_format,
        axislabels=((date_label, None)),
        mask_outside=True,
        raster=True,
    )
    # Adding noise power line if necessary
    if health_fig:
        plt.plot(times, 5 + mrm, "k-", label="Radiometric noise power")
        plt.axhline(y=15, color="k", linestyle="dashed")
        plt.legend(loc="upper right")
    if is_weekly_fig:
        plt.xlim(
            (
                datetime.strptime(
                    title[-12:] + " 1 00:00", "%G week %V %u %H:%M"
                ),
                datetime.strptime(
                    title[-12:] + " 7 23:59", "%G week %V %u %H:%M"
                ),
            )
        )
    else:
        plt.xlim(
            datetime.strptime(title[-10:] + " 00:00", "%Y-%m-%d %H:%M"),
            datetime.strptime(title[-10:] + " 23:59", "%Y-%m-%d %H:%M"),
        )
    plt.ylim((0, 18))
    display.plot_grid_lines()

    # Saving figure
    plt.savefig(figname + ".png", dpi=300, bbox_inches="tight")

    plt.clf()
    plt.close()
    gc.collect()
    del fig

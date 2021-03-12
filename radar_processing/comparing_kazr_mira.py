import matplotlib.pyplot as plt
import numpy as np
from glob import glob

import pyart

from read_mira_radar import read_multi_mira


# Reading files
# - Defining filepaths
kazr_ge = "data/radar/ka_cordoba/ge/"
kazr_md = "data/radar/ka_cordoba/md/"
a1 = "a1/"
b1 = "b1/"
mira = "data/radar/mira_campina/"

# - Find, selecting and reading files
# -- KAZR
files = sorted(os.listdir(kazr_ge + a1))
file_ge_a1 = list(filter(lambda date: "20181205.1800" in date, files))[0]
files = sorted(os.listdir(kazr_ge + b1))
file_ge_b1 = list(filter(lambda date: "20181205.1800" in date, files))[0]
files = sorted(os.listdir(kazr_md + a1))
file_md_a1 = list(filter(lambda date: "20181205.1800" in date, files))[0]
files = sorted(os.listdir(kazr_md + b1))
file_md_b1 = list(filter(lambda date: "20181205.1800" in date, files))[0]
kazr_ge_a1 = pyart.io.read(kazr_ge + a1 + file_ge_a1)
kazr_ge_b1 = pyart.io.read(kazr_ge + b1 + file_ge_b1)
kazr_md_a1 = pyart.io.read(kazr_md + a1 + file_md_a1)
kazr_md_b1 = pyart.io.read(kazr_md + b1 + file_md_b1)
# print(kazr_ge_a1.fields.keys())
# print(kazr_ge_b1.fields.keys())

# -- MIRA
month_day = "07//11/"
hours = ["11"]
ext = "00.mmclx"
files_mira = []
for hour in hours:
    files_mira.append(glob(mira + month_day + "*" + hour + ext).pop(0))
# print(files_mira)
# --- For more than one day
# month_day = "03/16/"
# hours = ["00"]
# for hour in hours:
#     files_mira.append(glob(mira + month_day + '*' + hour + ext).pop(0))
mira_b, mira_melt_hei = read_multi_mira(files_mira)
# print(mira_b.fields.keys())

# Plotting
# - KAZR
display = pyart.graph.RadarDisplay(kazr_ge_a1)
fig = plt.figure(figsize=(12, 5))
display.plot_vpt("reflectivity", vmin=-30, vmax=70, time_axis_flag=True)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/kazr_ge_a1_z.png", dpi=300, bbox_inches="tight"
)
plt.close()
fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "mean_doppler_velocity",
    vmin=-10,
    vmax=10,
    cmap="pyart_BuDRd18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/kazr_ge_a1_v.png", dpi=300, bbox_inches="tight"
)

display = pyart.graph.RadarDisplay(kazr_ge_b1)
fig = plt.figure(figsize=(12, 5))
display.plot_vpt("reflectivity", vmin=-30, vmax=70, time_axis_flag=True)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/kazr_ge_b1_z.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()
fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "mean_doppler_velocity",
    vmin=-10,
    vmax=10,
    cmap="pyart_BuDRd18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/kazr_ge_b1_v.png",
    dpi=300,
    bbox_inches="tight",
)

display = pyart.graph.RadarDisplay(kazr_md_a1)
fig = plt.figure(figsize=(12, 5))
display.plot_vpt("reflectivity", vmin=-30, vmax=70, time_axis_flag=True)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/kazr_md_a1_z.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()
fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "mean_doppler_velocity",
    vmin=-10,
    vmax=10,
    cmap="pyart_BuDRd18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/kazr_md_a1_v.png",
    dpi=300,
    bbox_inches="tight",
)

display = pyart.graph.RadarDisplay(kazr_md_b1)
fig = plt.figure(figsize=(12, 5))
display.plot_vpt("reflectivity", vmin=-30, vmax=70, time_axis_flag=True)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/kazr_md_b1_z.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()
fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "mean_doppler_velocity",
    vmin=-10,
    vmax=10,
    cmap="pyart_BuDRd18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/kazr_md_b1_v.png",
    dpi=300,
    bbox_inches="tight",
)

# - MIRA
# -- Modifying units before plot
mira_b.fields["SNRg"]["data"] = 10 * np.log10(mira_b.fields["SNRg"]["data"])
mira_b.fields["SNR"]["data"] = 10 * np.log10(mira_b.fields["SNR"]["data"])
mira_b.fields["Ze"]["data"] = 10 * np.log10(mira_b.fields["Ze"]["data"])
mira_b.fields["Zg"]["data"] = 10 * np.log10(mira_b.fields["Zg"]["data"])
mira_b.fields["Z"]["data"] = 10 * np.log10(mira_b.fields["Z"]["data"])
mira_b.fields["LDRg"]["data"] = 10 * np.log10(mira_b.fields["LDRg"]["data"])
mira_b.fields["LDR"]["data"] = 10 * np.log10(mira_b.fields["LDR"]["data"])
mira_b.fields["SNRg"]["units"] = "dBZ"

# Generating x-axis for Melting Layer Height
# print(mira_melt_hei[0]['data'])
times = pyart.util.datetimes_from_radar(mira_b)
times = times.astype("datetime64[ns]")

display = pyart.graph.RadarDisplay(mira_b)
fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "SNRg",
    vmin=mira_b.fields["SNRg"]["yrange"][0],
    vmax=mira_b.fields["SNRg"]["yrange"][1],
    cmap="pyart_Carbone17",
    time_axis_flag=True,
)
plt.plot(
    times,
    mira_melt_hei[0]["data"] / 1000,
    "k--",
    label=mira_melt_hei[0]["long_name"],
)
display.plot_grid_lines()
plt.legend(loc="upper right")
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_snrg.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "SNR",
    vmin=mira_b.fields["SNR"]["yrange"][0],
    vmax=mira_b.fields["SNR"]["yrange"][1],
    cmap="pyart_Carbone17",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_snr.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "Ze",
    vmin=mira_b.fields["Ze"]["yrange"][0],
    vmax=40,
    cmap="pyart_Theodore16",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_ze.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "Zg",
    vmin=mira_b.fields["Zg"]["yrange"][0],
    vmax=40,
    cmap="pyart_Theodore16",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_zg.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "Z",
    vmin=mira_b.fields["Z"]["yrange"][0],
    vmax=40,
    cmap="pyart_Theodore16",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_z.png", dpi=300, bbox_inches="tight"
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "RR",
    vmin=mira_b.fields["RR"]["yrange"][0],
    vmax=mira_b.fields["RR"]["yrange"][1],
    cmap="pyart_RRate11",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_rr.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "VELg",
    vmin=mira_b.fields["VELg"]["yrange"][0],
    vmax=mira_b.fields["VELg"]["yrange"][1],
    cmap="pyart_BuDRd18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_velg.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "VEL",
    vmin=mira_b.fields["VEL"]["yrange"][0],
    vmax=mira_b.fields["VEL"]["yrange"][1],
    cmap="pyart_BuDRd18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_vel.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "RHO",
    vmin=mira_b.fields["RHO"]["yrange"][0],
    vmax=mira_b.fields["RHO"]["yrange"][1],
    cmap="pyart_RefDiff",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_rho.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "RHOwav",
    vmin=mira_b.fields["RHOwav"]["yrange"][0],
    vmax=mira_b.fields["RHOwav"]["yrange"][1],
    cmap="pyart_RefDiff",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_rhowav.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "LDR",
    vmin=mira_b.fields["LDR"]["yrange"][0],
    vmax=mira_b.fields["LDR"]["yrange"][1],
    cmap="pyart_SCook18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_ldr.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "LDRg",
    vmin=mira_b.fields["LDRg"]["yrange"][0],
    vmax=mira_b.fields["LDRg"]["yrange"][1],
    cmap="pyart_SCook18",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_ldrg.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "DPS",
    vmin=mira_b.fields["DPS"]["yrange"][0],
    vmax=mira_b.fields["DPS"]["yrange"][1],
    cmap="pyart_Wild25",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_dps.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "DPSwav",
    vmin=mira_b.fields["DPSwav"]["yrange"][0],
    vmax=mira_b.fields["DPSwav"]["yrange"][1],
    cmap="pyart_Wild25",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_dpswav.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "LWC",
    vmin=mira_b.fields["LWC"]["yrange"][0],
    vmax=mira_b.fields["LWC"]["yrange"][1],
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_lwc.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "RMSg",
    vmin=mira_b.fields["RMSg"]["yrange"][0],
    vmax=mira_b.fields["RMSg"]["yrange"][1],
    cmap="pyart_NWS_SPW",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_rmsg.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

fig = plt.figure(figsize=(12, 5))
display.plot_vpt(
    "RMS",
    vmin=mira_b.fields["RMS"]["yrange"][0],
    vmax=mira_b.fields["RMS"]["yrange"][1],
    cmap="pyart_NWS_SPW",
    time_axis_flag=True,
)
plt.ylim((0, 18))
plt.savefig(
    "radar_processing/figs/mira_kazr/mira_b_rms.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()


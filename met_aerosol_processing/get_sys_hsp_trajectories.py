# Using HYSPLIT backward trajectories to estimate initial conditions around CSs

# HYSPLIT output provided by IFUSP
# http://ftp.lfa.if.usp.br/ftp/public/LFA_Processed_Data/hysplit/gdas0p5_12min/backward/ascii_files/

# CSs data from systems_filtered table


import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas as pd
import geopandas as gpd
from shapely import wkb


def join_hst_sys(hst, sysfilt, maxdistance):
    """
    Match HYSPLIT trajectories and CSs in space.
    Conditions:
        - Backward trajectories only up to 6h
        - Interval between CS timestamp and trajectories points <= 6h

    Parameters
    ----------
    hst: geopandas.geodataframe
        HYSPLIT data points
    sysfilt: pandas.Series
        CS row from systems_filtered dataframe
    maxdistance: float
        Maximum distance between geometries in meters

    Returns
    -------
    result: pandas.Series

    """

    # Changing CRS to pseudo-Mercator for calculations
    geo_sysfilt = gpd.GeoDataFrame(
        sysfilt.to_frame().T,
        geometry=sysfilt.to_frame().T.geom,
        crs="EPSG:4326",
    ).to_crs(crs=3857)
    hst.to_crs(crs=3857, inplace=True)
    # Interval between CS timestamp and trajectories points
    inter = abs(geo_sysfilt.iloc[0].timestamp - hst.date)
    # Extract data within intervals <= 6h
    hst = hst.loc[inter[inter <= pd.Timedelta(6, "H")].index]
    # Match in space, return to geographical coordinates
    pts_within = (
        hst.sjoin_nearest(
            geo_sysfilt, max_distance=maxdistance, distance_col="distance"
        )
        .reset_index()
        .to_crs(crs="EPSG:4326")
    )
    # Interval between CS timestamp and trajectories points
    pts_within["inter"] = abs(pts_within.timestamp - pts_within.date)
    # Match in time, get minimum interval
    pts_within2 = pts_within.loc[
        pts_within.groupby("date_hours")["inter"].idxmin()
    ].loc[pts_within.inter < pd.Timedelta(6, "H")]
    # print(pts_within2)
    # Return row with data or with zeros
    if not pts_within2.empty:
        result = pts_within2.loc[pts_within2["date_hours"].idxmax()]
    else:
        result = pts_within2.append(
            pd.Series(0, index=pts_within2.columns), ignore_index=True
        ).iloc[0]
    print("done - system", sysfilt.geom_name)
    return result


# Reading HYSPLIT trajectories
df1 = pd.read_csv(
    "/home/camilacl/git/amazon-storms-aerosols/data/general/hysplit_2014_backward_paths.csv",
    index_col=[-1],
)
df2 = pd.read_csv(
    "/home/camilacl/git/amazon-storms-aerosols/data/general/hysplit_2015_backward_paths.csv",
    index_col=[-1],
)
# Joining 2014 and 2015 data, remove trajectories longer than 6h
hst_bwd = pd.concat([df1, df2])
hst_bwd = hst_bwd.loc[hst_bwd.date_hours >= -6]
# Converting to geodataframe
geo_hst_bwd = gpd.GeoDataFrame(
    hst_bwd,
    geometry=gpd.points_from_xy(hst_bwd.lon, hst_bwd.lat),
    crs="EPSG:4326",
)
# Converting dates to local time
geo_hst_bwd.date = pd.to_datetime(geo_hst_bwd.date)
geo_hst_bwd.date = geo_hst_bwd.date.dt.tz_convert("America/Manaus")
# Renaming col
geo_hst_bwd.index.names = ["name_file"]
print("HYSPLIT trajectories read!")

# Removing trajectories within Manaus plume (30-km radius around INPA)
# - INPA coordinates
coords = pd.DataFrame({"lon": [-59.9867], "lat": [-3.0972]})
geo_coords = gpd.GeoDataFrame(
    coords, geometry=gpd.points_from_xy(coords.lon, coords.lat), crs="EPSG:4326"
)
# - Match with trajectories
trajs_within_manaus = (
    geo_hst_bwd.to_crs(crs=3857)
    .sjoin_nearest(
        geo_coords.to_crs(crs=3857), max_distance=30000, distance_col="distance"
    )
    .index.unique()
)
# - Removing trajectories
geo_hst_bwd = geo_hst_bwd.loc[~geo_hst_bwd.index.isin(trajs_within_manaus)]
print("Trajectories within Manaus plume removed!")

# Reading systems data
df = pd.read_pickle(
    "/home/camilacl/git/amazon-storms-aerosols/data/general/systems_filtered_sg_v1.pickle"
)
# Converting to geodataframe
df.geom = [wkb.loads(bytes(g.ExportToWkb())) for g in df.geom]
sys_filt = gpd.GeoDataFrame(df, geometry="geom", crs="EPSG:4326")
print("Systems read!")

# Applying matching function
sys_hsp = sys_filt.apply(
    lambda row: join_hst_sys(geo_hst_bwd, row, 10000), axis=1
)

# Saving to pickle file
sys_hsp.loc[sys_hsp.name_file != 0].to_pickle(
    "/home/camilacl/git/amazon-storms-aerosols/data/general/sysfilt_hstbwd_nearest_6h_10km.pickle"
)

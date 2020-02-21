"""
Reading and writing Grid objects.

"""

import datetime
import warnings

import netCDF4
import numpy as np

from pyart.core.grid import Grid
from pyart.io.cfradial import _ncvar_to_dict, _create_ncvar
from pyart.io.common import _test_arguments


def read_grid(filename, exclude_fields=None, include_fields=None, **kwargs):
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
    _test_arguments(kwargs)

    if exclude_fields is None:
        exclude_fields = []

    reserved_variables = [
        'time', 'x', 'y', 'z',
        'origin_latitude', 'origin_longitude', 'origin_altitude',
        'point_x', 'point_y', 'point_z', 'projection',
        'point_latitude', 'point_longitude', 'point_altitude',
        'radar_latitude', 'radar_longitude', 'radar_altitude',
        'radar_name', 'radar_time', 'base_time', 'time_offset',
        'ProjectionCoordinateSystem']

    dset = netCDF4.Dataset(filename, mode='r')

    # metadata
    metadata = dict([(k, getattr(dset, k)) for k in dset.ncattrs()])

    # required reserved variables
    time = _ncvar_to_dict(dset.variables['time'])
    origin_latitude = _ncvar_to_dict(
        dset.variables['grid_mapping_0'].latitude_of_projection_origin)
    origin_longitude = _ncvar_to_dict(
        dset.variables['grid_mapping_0'].longitude_of_projection_origin)
    origin_altitude = None
    x = _ncvar_to_dict(dset.variables['x0'])
    y = _ncvar_to_dict(dset.variables['y0'])
    z = _ncvar_to_dict(dset.variables['z0'])

    # projection
    projection = _ncvar_to_dict(
        dset.variables['grid_mapping_0'].grid_mapping_name)
    projection.pop('data')
    # map _include_lon_0_lat_0 key to bool type
    if '_include_lon_0_lat_0' in projection:
        v = projection['_include_lon_0_lat_0']
        projection['_include_lon_0_lat_0'] = {'true': True, 'false': False}[v]

    # read in the fields
    fields = {}

    # fields in the file has a shape of (1, nz, ny, nx) with the leading 1
    # indicating time but should shaped (nz, ny, nx) in the Grid object
    field_shape = tuple([len(dset.dimensions[d]) for d in ['z', 'y', 'x']])
    field_shape_with_time = (1, ) + field_shape

    # check all non-reserved variables, those with the correct shape
    # are added to the field dictionary, if a wrong sized field is
    # detected a warning is raised
    field_keys = [k for k in dset.variables if k not in reserved_variables]
    for field in field_keys:
        if field in exclude_fields:
            continue
        if include_fields is not None:
            if field not in include_fields:
                continue
        field_dic = _ncvar_to_dict(dset.variables[field])
        if field_dic['data'].shape == field_shape_with_time:
            field_dic['data'].shape = field_shape
            fields[field] = field_dic
        else:
            bad_shape = field_dic['data'].shape
            warnings.warn(
                'Field %s skipped due to incorrect shape %s'
                % (field, bad_shape))

    # radar_ variables
    if 'radar_latitude' in dset.variables:
        radar_latitude = _ncvar_to_dict(dset.variables['radar_latitude'])
    else:
        radar_latitude = None

    if 'radar_longitude' in dset.variables:
        radar_longitude = _ncvar_to_dict(dset.variables['radar_longitude'])
    else:
        radar_longitude = None

    if 'radar_altitude' in dset.variables:
        radar_altitude = _ncvar_to_dict(dset.variables['radar_altitude'])
    else:
        radar_altitude = None

    if 'radar_name' in dset.variables:
        radar_name = _ncvar_to_dict(dset.variables['radar_name'])
    else:
        radar_name = None

    if 'radar_time' in dset.variables:
        radar_time = _ncvar_to_dict(dset.variables['radar_time'])
    else:
        radar_time = None

    dset.close()

    return Grid(
        time, fields, metadata,
        origin_latitude, origin_longitude, origin_altitude, x, y, z,
        projection=projection,
        radar_latitude=radar_latitude, radar_longitude=radar_longitude,
        radar_altitude=radar_altitude, radar_name=radar_name,
        radar_time=radar_time)


def _make_coordinatesystem_dict(grid):
    """
    Return a dictionary containing parameters for a coordinate transform.

    Examine the grid projection attribute and other grid attributes to
    return a dictionary containing parameters which can be written to a netCDF
    variable to specify a horizontal coordinate transform recognized by
    Unidata's CDM. Return None when the projection defined in the grid
    cannot be mapped to a CDM coordinate transform.
    """
    projection = grid.projection
    origin_latitude = grid.origin_latitude['data'][0]
    origin_longitude = grid.origin_longitude['data'][0]
    cdm_transform = {
        'latitude_of_projection_origin': origin_latitude,
        'longitude_of_projection_origin': origin_longitude,
        '_CoordinateTransformType': 'Projection',
        '_CoordinateAxes': 'x y z time',
        '_CoordinateAxesTypes': 'GeoX GeoY Height Time',
    }

    if projection['proj'] == 'ortho':
        cdm_transform['grid_mapping_name'] = 'orthographic'

    elif projection['proj'] == 'laea':
        cdm_transform['grid_mapping_name'] = 'lambert_azimuthal_equal_area'

    elif projection['proj'] in ['aeqd', 'pyart_aeqd']:
        cdm_transform['grid_mapping_name'] = 'azimuthal_equidistant'
        # CDM uses a ellipsoid where as PyProj uses a sphere by default,
        # therefore there will be slight differences in these transforms
        cdm_transform['semi_major_axis'] = 6370997.0
        cdm_transform['inverse_flattening'] = 298.25  # proj uses a sphere
        cdm_transform['longitude_of_prime_meridian'] = 0.0
        cdm_transform['false_easting'] = 0.0
        cdm_transform['false_northing'] = 0.0

    elif projection['proj'] == 'tmerc':
        cdm_transform['grid_mapping_name'] = 'transverse_mercator'
        cdm_transform['longitude_of_central_meridian'] = origin_longitude
        cdm_transform['scale_factor_at_central_meridian'] = 1.00

    elif projection['proj'] == 'lcc':
        cdm_transform['grid_mapping_name'] = 'lambert_conformal_conic'
        cdm_transform['standard_parallel'] = origin_latitude
        cdm_transform['longitude_of_central_meridian'] = origin_longitude

    elif projection['proj'] == 'aea':
        cdm_transform['grid_mapping_name'] = 'albers_conical_equal_area'
        cdm_transform['standard_parallel'] = origin_latitude
        cdm_transform['longitude_of_central_meridian'] = origin_longitude

    elif projection['proj'] == 'stere':
        cdm_transform['grid_mapping_name'] = 'stereographic'
        cdm_transform['scale_factor_at_projection_origin'] = 1.00

    elif projection['proj'] in ['npstere', 'spstere']:
        cdm_transform['grid_mapping_name'] = 'polar_stereographic'
        cdm_transform['standard_parallel'] = origin_latitude

    # 'cea' may be able to map to 'lambert_cylindrical_equal_area' and
    # 'merc' to 'mercator' but both projections seems to always be
    # centered at the equator regardless of the value of the
    # standard_parallel parameter
    else:
        cdm_transform = None

    return cdm_transform

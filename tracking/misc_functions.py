# -*- coding: utf-8 -*-
"""
MISCELLANEOUS FUNCTIONS

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

import numpy as np
import pickle
from matplotlib.colors import LinearSegmentedColormap


def save_object(obj, filename):
    """
    Saving python objects in a file.

    Parameters
    ----------
    obj: python object
    filename: name of the saved file
    """

    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def open_object(filename):
    """
    Open python object saved in a file.

    Parameters
    ----------
    filename: name of the saved file

    Returns
    -------
    obj: python object
    """

    with open(filename, 'rb') as input:
        obj = pickle.load(input)

    return obj


def check_sounding_for_montonic(sounding):
    """
    Force sounding data to be monotonic.

    Parameters
    ----------
    sounding: SkewT sounding

    Returns
    -------
    snd_T, snd_z: sounding temperature and height
    """
    snd_T = sounding['temperature']
    snd_z = sounding['height']  # In old SkewT, was sounding.data
    dummy_z = []
    dummy_T = []
    if not snd_T.mask[0]:  # May cause issue for specific soundings
        dummy_z.append(snd_z[0])
        dummy_T.append(snd_T[0])
        for i, height in enumerate(snd_z):
            if i > 0:
                if snd_z[i] > snd_z[i-1] and not snd_T.mask[i]:
                    dummy_z.append(snd_z[i])
                    dummy_T.append(snd_T[i])
        snd_z = np.array(dummy_z)
        snd_T = np.array(dummy_T)
    return snd_T, snd_z


def make_colormap(seq, name, n=256):
    """
    Create a LinearSegmentedColormap from a sequence of colors

    Parameters
    ----------
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
        and in the interval (0,1)
    name: name of the colormap

    Returns
    -------
    LinearSegmentedColormap
    """

    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return LinearSegmentedColormap(name, cdict, N=n)

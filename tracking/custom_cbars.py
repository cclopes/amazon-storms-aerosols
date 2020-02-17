# -*- coding: utf-8 -*-
"""
CREATE CUSTOM COLORBARS

@author: Camila Lopes (camila.lopes@iag.usp.br)
"""

# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ColorConverter

from misc_functions import make_colormap

converter = ColorConverter().to_rgb

cmap = make_colormap([converter("#99CCFF"), converter("#18A04C"), 0.35,
                      converter("#18A04C"), converter("#FFDF8E"), 0.55,
                      converter("#FFDF8E"), 0.6,
                      converter("#FFDF8E"), converter("#D64646"), 0.85,
                      converter("#D64646"), converter("#0F0D0D")],
                     'dbz', n=15)
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#20314C"), converter("#7AADFF"), 0.2,
                      converter("#7AADFF"), converter("#F9F9F9"), 0.3,
                      converter("#F9F9F9"), 0.33,
                      converter("#F9F9F9"), converter("#F48244"), 0.45,
                      converter("#F48244"), converter("#470219")],
                     'zdr', n=17)
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#224C25"), converter("#CAE894"), 0.3,
                      converter("#CAE894"), converter("#F9F9F9"), 0.38,
                      converter("#F9F9F9"), 0.4,
                      converter("#F9F9F9"), converter("#AF95E2"), 0.55,
                      converter("#AF95E2"), converter("#3E0B5E")],
                     'kdp', n=17)
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#FFF0E2"), converter("#DDA65D"), 0.5,
                      converter("#DDA65D"), converter("#B21152"), 0.75,
                      converter("#B21152"), converter("#442F42"), 0.99,
                      converter("#CCB69B")],
                     'rho', n=17)
plt.register_cmap(name=cmap.name, cmap=cmap)

cmap = make_colormap([converter("#FFFFFF"), converter("#CBEDCA"), 0.1,
                      converter("#CBEDCA"), converter("#77CFBE"), 0.35,
                      converter("#77CFBE"), converter("#0A92AC"), 0.7,
                      converter("#0A92AC"), converter("#2D3184")],
                     'mass', n=15)
plt.register_cmap(name=cmap.name, cmap=cmap)

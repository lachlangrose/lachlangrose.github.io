"""
============================
Building an implicit surface
============================
This tutorial will demonstrate how to create an implicit surface representation of surfaces from a combination of orientation and location observations.

Implicit surface representation involves finding an unknown function where $f(x,y,z)$ matches observations of the surface geometry. We generate a scalar field where the scalar value is the distance away from a reference horizon. The reference horizon is arbritary and can either be:

 * a single geological surface where the scalar field would represent the signed distance away from this surface. (above the surface positive and below negative)
 * Where multiple conformable horizons are observed the same scalar field can be used to represent these surfaces and the thickness of the layers is used to determine the relative scalar value for each surface


This tutorial will demonstrate both of these approaches for modelling a number of horizons picked from seismic data sets.
"""
from LoopStructural import GeologicalModel
from LoopStructural.visualisation import LavaVuModelViewer

from LoopStructural.datasets import load_claudius #demo data

import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import logging
logging.getLogger().setLevel(logging.INFO)
data, bb = load_claudius()
model = GeologicalModel(bb[0, :], bb[1, :])
model.set_model_data(data)
# print(data['type'])
s0 = model.create_and_add_foliation('strati',
                                    interpolatortype='PLI',
                                    nelements=1000,
                                    solver='cg',
                                    damp=False)
print(len(s0['feature'].get_interpolator().row))
newrows = s0['feature'].get_interpolator().remove_constraints_from_least_squares(name='regularisation')
print(newrows.shape)
plt.plot(np.unique(newrows))
plt.show()
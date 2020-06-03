"""
Faulted folds
===============

"""


######################################################################
# Faulted refolded folds
# ======================
# 


######################################################################
# Imports
# ~~~~~~~
# 

import sys, os, subprocess
import matplotlib.pyplot as plt
# adjust some settings for matplotlib
from matplotlib import rcParams
import numpy as np
import scipy
import scipy.fftpack
from LoopStructural.visualisation import LavaVuModelViewer
from LoopStructural.utils.helper import strike_dip_vector
from LoopStructural import GeologicalModel
import LoopStructural
import pandas as pd
# print rcParams
rcParams['font.size'] = 15
# determine path of repository to set paths corretly below
repo_path = os.path.realpath('../..')
sys.path.append(repo_path)
import pynoddy.history
import logging
logging.getLogger().setLevel(logging.INFO)


######################################################################
# Load data and define model box
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

df2 = pd.read_csv('faulted_type1.csv')
bb = np.zeros((2,3))
bb[1,:] =(10000.0, 7000.0, 5000.0)


######################################################################
# View the data
# ~~~~~~~~~~~~~
# 
# Have a look at the contents of the data frame, we can see there are a
# number of columns e.g strike, dip, value, coord, type etc. These are
# used by LoopStructural to constrain the interpolator. The column type
# contains our identifier for which scalar field the data points are
# constraining e.g. the fault, s1 or s0.
# 

df2

df2.type.unique()


######################################################################
# Setting up the model
# ~~~~~~~~~~~~~~~~~~~~
# 
# Below we can set up the model, first we need to know which order these
# geological features occured. In this example the fault is the most
# recent feature, and then the s1 foliation and then the primary foliation
# (s0).
# 
# Therefore to create the model we add these features in the reverse
# order: 1. Fault 2. s1 3. s0
# 


######################################################################
# Creating the fault frame
# ~~~~~~~~~~~~~~~~~~~~~~~~
# 

model = GeologicalModel(bb[0,:],bb[1,:])
model.set_model_data(df2)
model.data

fault = model.create_and_add_fault('fault',
                                   -500,
                                   nelements=2e4,
                                   interpolatottype='PLI',
                                   buffer=0.7,
                                   solver='lu',
                                   damp=True
                                  )
viewer = LavaVuModelViewer(model)
viewer.add_isosurface(fault['feature'][0],
                     isovalue=0
                     )
viewer.add_vector_field(fault['feature'][1],locations=model.regular_grid()[::50])
viewer.interactive()


######################################################################
# Creating the fold frame
# ~~~~~~~~~~~~~~~~~~~~~~~
# 

fold_frame = model.create_and_add_fold_frame('s1',
                                nelements=1e4,
                                            regularisation=[1.,1.,.1],
                                            interpolatortype='PLI',
#                                             gxxgy=0.,
                                            solver='lu',
                                            damp=True,
                                            buffer=0.7)

viewer = LavaVuModelViewer(model)
viewer.add_isosurface(fault['feature'][0],
                     isovalue=0)
viewer.add_isosurface(fold_frame['feature'][0],
                     isovalue=0)
viewer.interactive()



######################################################################
# Interpolating bedding
# ~~~~~~~~~~~~~~~~~~~~~
# 

s0 = model.create_and_add_folded_foliation('s0',
                                           fold_frame=fold_frame['feature'],
                                      nelements=1e4,
                                          solver='lu',
                                          buffer=0.5,
                                          damp=True)
viewer = LavaVuModelViewer(model)

viewer.add_vector_field(fold_frame['feature'][1],
                       locations=s0['feature'].builder.interpolator.get_gradient_constraints()[:,:3]
                       )


viewer.add_isosurface(fold_frame['feature'][1],
                     isovalue=0)

viewer.add_data(fold_frame['feature'][1])

viewer.add_scalar_field(s0['feature'],cmap='tab20')

viewer.add_isosurface(s0['feature'])
viewer.add_data(s0['feature'])
viewer.interactive()

viewer.lv.image('images\example5.png')


######################################################################
# Fold axis rotation angle
# ~~~~~~~~~~~~~~~~~~~~~~~~
# 

fig, ax = plt.subplots(1,2,figsize=(10,5),)
x = np.linspace(fold_frame['feature'][1].min(),fold_frame['feature'][1].max(),100)
ax[0].plot(s0['axis_direction'],s0['axis_rotation'],'bo')
ax[0].plot(x, s0['fold'].fold_axis_rotation(x),'b-')
ax[0].set_ylabel('Fold axis rotation angle')
ax[0].set_xlabel('Fold frame coordinate 1 value')


ax[1].plot(s0['axis_svariogram'].lags,s0['axis_svariogram'].variogram,'ko')
ax[1].set_ylabel('Fold axis variogram')
ax[1].set_xlabel('S-Variogram lags')


ax[0].set_ylim(-90,90)


######################################################################
# Fold limb rotation angle
# ~~~~~~~~~~~~~~~~~~~~~~~~
# 

fig, ax = plt.subplots(1,2,figsize=(10,5),)
x = np.linspace(fold_frame['feature'][1].min(),fold_frame['feature'][1].max(),100)
ax[0].plot(s0['foliation'],s0['limb_rotation'],'bo')
ax[0].plot(x, s0['fold'].fold_limb_rotation(x),'b-')
ax[0].set_ylabel('Fold axis rotation angle')
ax[0].set_xlabel('Fold frame coordinate 1 value')


ax[1].plot(s0['limb_svariogram'].lags,s0['limb_svariogram'].variogram,'ko')
ax[1].set_ylabel('Fold axis variogram')
ax[1].set_xlabel('S-Variogram lags')


ax[0].set_ylim(-90,90)


from LoopStructural.visualisation import MapView
mapview = MapView(model)
mapview.nsteps = np.array([40,40])
mapview.add_data(s0['feature'],scale=0.02)
mapview.add_scalar_field(s0['feature'],cmap='tab20')
mapview.add_contour(s0['feature'],4)
mapview.add_contour(fault['feature'][0],[0])
plt.xlim(model.bounding_box[0,0],model.bounding_box[1,0])
plt.ylim(model.bounding_box[0,1],model.bounding_box[1,1])


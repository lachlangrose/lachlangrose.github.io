---
title: LoopStructural 1.0 Time aware geological modelling
authors: Lachlan Grose, Laurent Ailleres, Gautier Laurent and Mark Jessell
year: 2020
journal: GMD Discussions
doi: <a href="https://doi.org/10.5194/gmd-2020-336">10.5194/gmd-2020-336</a>
citation: Grose et al., 2020
---
In this contribution we introduce LoopStructural, a new open source 3D geological modelling python package ( https://www.github.com/Loop3d/LoopStructural). LoopStructural provides a generic API for 3D geological modelling applications harnessing the core python scientific libraries pandas, numpy and scipy. Six different interpolation algorithms, including 3 discrete interpolators and 3 polynomial trend interpolators, can be used from the same model design. This means that different interpolation algorithms can be mixed and matched within a geological model allowing for different geological objects e.g. different conformable foliations, fault surfaces, unconformities to be modelled using different algorithms. Geological features are incorporated into the model using a time-aware approach, where the most recent features are modelled first and used to constrain the geometries of the older features. For example, we use a fault frame for characterising the geometry of the fault surface and apply each fault sequentially to the faulted surfaces. In this contribution we use LoopStructural to produce synthetic proof of concepts models and a 86 x 52 km model of the Flinders ranges in South Australia using map2loop.



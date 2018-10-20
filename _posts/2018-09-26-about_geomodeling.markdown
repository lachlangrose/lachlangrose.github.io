---
layout: post
title:  "About structural geological modelling"
date:   2018-09-26 09:39:19 +1000
categories: research 3d-modeling
---
3D geological models are a subsurface representation of geological features: e.g. stratigraphy, faults, unconformities and folds.  The geometries represented in the 3D model represents the result of deformational events but not the process of deforming the rocks, in structural geology this is the finite strain.

We build 3D geological models by summarising and interpreting between geological observations, usually the type of rock, the orientation of the rock packages and the location of any structures e.g. faults and folds. There are a range of approaches that are used to go from sparse, typically 2-D observations to a 3D representation of the geology.  This involves interpolating between observations and extrapolating away from observations. Most geological models are built by building surfaces that represent the contact between stratigraphic units – these can either be represented using an explicit support: where the geometry of the surface is stored in the representation of the surface (e.g. a triangulated surface where the node values represent the surface location in space); or using an implicit support where the surface geometry is represented as an isovalue of an implicit function in 3D space. The implicit approach is generally favoured because it allows for easy updating of surface geometry with additional data or interpretation and the support does not change by the topological interaction between geological features. For example, the scalar field representing an older fault that is overprinted by younger fault does not change if the geometry of the younger fault changes or if the topological relationship is changed.

The crux of the implicit modelling approach is how to generate a scalar field that represents the geometry of deformed rocks from sparse data sets.

There are two main approaches that are typically used:
- Polynomial trend algorithms 
- Discrete implicit approach

## Polynomial trend
Polynomial trend methods use a weighted combination of a global polynomial terms and local kernel to generate a scalar field where the isosurfaces represent the geometry of the geological units. Polynomial trend methods include co-kriging and radial basis function interpolations. Both methods combine the global polynomial trend as a drift function with local kernels representing the variance in property value between pairs of points. Observations for the orientation of the surface constrain the gradient of the interpolant and observations of the stratigraphy constrain the value of the scalar field.
## Discrete implicit approach
Discrete implicit modelling involves approximating a piecewise linear scalar field on a 3D tetrahedron mesh. The model area is represented by a regular grid of 4 node tetrahedron elements. The 4 node tetrahedron has a constant gradient within element meaning interpolated scalar field varies linearly between nodes of the element. The geological observations and spatial continuity is expressed as linear equations that are solved to find the optimal values of the mesh nodes. The spatial continuity is represented by a regularisation term which minimises the variation in the gradient of the scalar field for neighbouring tetrahedron elements.

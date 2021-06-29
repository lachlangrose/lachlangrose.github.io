---
layout: posts
title:  "New paper: Realistic modelling of faults in LoopStructural"
date:   2021-06-13 20:39:54 +1000
# categories: papers
classes: wide
author: Lachlan Grose
author_profile: true
excerpt_separator: <!--more--> 
---
We recently submitted another paper to the Loop3D special issue in Geoscientific Model Development. The paper is currently in discussion phase of the peer review but you can download it [here](https://gmd.copernicus.org/preprints/gmd-2021-112/gmd-2021-112.pdf).

The paper provides a conceptual and technical overview of how faults are incorporated into 3D models inside LoopStructural. This involves building a curvilinear coodinate system (fault frame) for the fault using the fault surface, fault slip direction and the fault extent. Within the fault frame the geometry displacement is defined by combining three functions describing the displacement within the fault ellispoid. The kinematics of the fault are characterised by gradient of the fault slip direction coordinate multiplied by the fault displacement. Faults are incorporated into the model by modelling the most recent fault first and using the kinematics of this fault to restore any feature overprinted by this fault. This is done before interpolating the older feature and the same function is used to incorporate the fault into the faulted surface.
---
layout: posts
title:  "New release: LoopStructural 1.1"
date:   2021-06-13 20:39:54 +1000
categories: loopstructural
classes: wide
author: Lachlan Grose
author_profile: true
excerpt_separator: <!--more--> 
---

The most recent version of LoopStructural addresses some minor bugs and adds a few small improvements for visualisation. The major changes are:
1. Faults added from map2loop are now added as *splay* or *abutting*
2. The default interpolator has been changed to Finite-Difference Interpolator, rather than Piecewise Linear Interpolator. 
3. The default solver for the least squares problem is conjugate gradient and the tolerance of the solver is scaled to the size of the model. This has significantly improved the speed of LoopStructural. There is no benefit to solving the least squares problem to 1e-12 when the value of the coefficients are greater than 1e4. Due to the changes in how faults are implemented pyamg is not recommended as the algorithmic multigrid algorithm is unable to extract the pattern from the interpolation matrix when lagrange multipliers are used.
4. Documentation is automatically built for each new release with a changelog generated using git-changelog

Other minor changes are outlined on the documentation changelog [here](https://loop3d.github.io/LoopStructural/changelog.html).

To install LoopStructural `pip install LoopStructural` or `conda install -c loop3d -c conda-forge LoopStructural`

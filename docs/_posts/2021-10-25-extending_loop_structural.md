---
layout: posts
title:  "Extending LoopStructural: adding iterative gradient norm constraints"
date:   2021-10-21 20:39:54 +1000
categories: programming
classes: wide
author: Lachlan Grose
author_profile: true
excerpt_separator: <!--more--> 
---
LoopStructural is the open source 3D geological modelling library that is the 3D modelling module of the Loop project. 
The code has been written in an object oriented modular format to make it easy to add functionalities and to extend the codebase.
In this blog post I will demonstrate the steps that were required to implement an iterative gradient norm constraint that was suggested by Gautier Laurent.

Gradient norm collapse
----------------------
The problem that we are trying to solve is the change in the magnitude of the gradient norm of the implicit function, as a result of overconstrained gradients.
This was identified in Gautier Laurents 2016 paper "Iterative Thickness Regularization of Stratigraphic Layers in Discrete Implicit Modeling" published in Mathematical Geosciences. 

Within discrete implicit modelling the gradient of the implicit function $ \nabla \phi(x,y,z) $ can be expressed as:

$$ \nabla \phi(x,y,z) = \textbf{T} \cdot \phi_c $$

where $\textbf{T}$ is a matrix representing the derivative of the shapefunction (e.g. linear tetrahedron) and the Jacobian of the coordinate transformation and $\phi_c$ are the values of the vertices of the discrete mesh. 

The norm of the implicit function is:
$$ |\nabla \phi|^2 = \nabla \phi ^T \cdot \nabla \phi = \phi_c^T \cdot \textbf{T}^T \cdot \textbf{T} \cdot \phi_c $$

This equation is quadratic and cannot easily be incorporated into the linear approach for solving the implicit models. 

Gautier's solution was approximate the gradient norm by using an estimation of the direction of the gradient ($u$) to constrain the norm of the implicit function. 

$$ || \nabla \phi || \approx \textit{u}^T \cdot \textbf{T} \cdot \phi_c = \frac{1}{L} $$

This constraint can be applied iteratively where the implicit function is evaluated without the gradient norm constraint and this is applied iteratively, either increasing the weight or increasing the number of constraints. 
In this post I will demonstrate how this was added into LoopStructural.

LoopStructural discrete interpolation
-------------------------------------
LoopStructural implements two discrete implicit modelling approaches:
1) using a tetrahedron support where the regularisation minimises the variation in the implicit function gradient between neighbouring elements.
2) using a Cartesian grid where the regularisation is a minimisation of the second derivative 


Both of these discrete interpolators share the same base class, **DiscreteInterpolator**, which manages the assembly of the least squares system and solving of the least squares problem.
When a constraint is added to the implicit function the method *add_constraint_to_least_squares* is called taking the value of the constraint, the node index of the constraint and the right hand side of the equation.
The implicit function is solved by assembling a sparse (MxN) matrix where M is the number of constraints and N is the number of degrees of freedom.

The implicit function is:
$$ A \cdot \phi_c = B$$

and can be solved in a least squares sense

$$ A^T \cdot A \cdot A^T \cdot B = \phi_c$$ 

In LoopStructural v1.3.7 the linear equations were solved when *._solve(solver='cg',**kwargs)* was called.

{% highlight python %}
logger.info("Solving interpolation for {}".format(self.propertyname))
self.c = np.zeros(self.support.n_nodes)
self.c[:] = np.nan
damp = True
if 'damp' in kwargs:
    damp = kwargs['damp']
if solver == 'lu':
    logger.info("Forcing matrix damping for LU")
    damp = True
if solver == 'lsqr':
    A, B =  self.build_matrix(False)
else:
    A, B = self.build_matrix(damp=damp)
## runs appropriate solver given solver argument
{% endhighlight %}

Adding constant norm
--------------------
To implement the constraints that Gautier suggests we need to apply the following algorithm
1. Build implicit system using classical constraints
2. Evaluate gradient of implicit function for mesh elements
3. Add constraint 
$$\frac{\nabla \phi}{|\nabla \phi|} \cdot \textbf{T} = \frac{1}{L}$$
4. Solve implicit function, go back to 2.

We can do this by defining a function
{% highlight python %}
def constant_norm(feature):
    # find centre of element and calculate gradient
    bc = feature.interpolator.support.barycentre()
    element_gradients = feature.interpolator.support.get_element_gradients()

    v = feature.evaluate_gradient(bc)
    v/=np.linalg.norm(v,axis=1)[:,None]
    T = feature.interpolator.support.calc_T(bc)
    bc = feature1.interpolator.support.barycentre()
    # calculate gradient for every element for previous iteration

    # get vert indexes for all elements
    elements = feature.interpolator.support.get_elements()
    vertices = feature.interpolator.support.nodes[feature.interpolator.support.get_elements()]
    vecs = vertices[:, 1:, :] - vertices[:, 0, None, :]
    vol = np.abs(np.linalg.det(vecs))  # / 6
    # previous iteration gradient \cdot current iteration T1
    a = np.einsum('ij,ijk->ik', v, element_gradients[:,:,:])
    # weighting by volume was causing odd results
    a *= vol[pairs[:,0], None]
    idc = elements
    B = np.zeros(a.shape[0])
    rows = np.tile(np.arange(a.shape[0]),(a.shape[1],1)).T
    A = coo_matrix((a.flatten(), (rows.flatten(), idc.flatten())),
                     shape=(a.shape[0], feature.interpolator.nx),
                       dtype=float)
    ATA = A.T.dot(A)
    ATB = A.T.dot(B)
    return ATA,ATB
{% endhighlight %}

This can then be applied iteratively to the model:

{% highlight python %}
def iterative_constant_norm(feature,ninter):
    from scipy.sparse.linalg import cg, splu
    # solve without constant norm
    feature.interpolator.solve_system(solver='cg',tol=feature1.builder.build_arguments['tol']) 
    for i in range(1,niter):
        print('iteration: {}'.format(i))
        A, B = feature.interpolator.build_matrix()
        # calculate constant norm
        ATA, ATB = constant_norm(feature)
        # increase weight for each iteration
        ATA*=w*((i**2+1)/(niter**2))
        # combine base matrix and constant norm matrix
        A+= ATA
        B+= ATB
        # solve using conjugate gradient
        soln = cg(A,B,tol=f.builder.build_arguments['tol'])
        # update feature node values
        f.interpolator.c = soln[0]
             
{% endhighlight %}

To add the gradient norm constraints we need to be able to modify the A matrix and B matrix between iterations to update 

To add the constraints for the gradient magnitude norm the re solved using the *_solve(A,B,solver='cg')* method which is called from *solve*.
To add the gradient norm constraints we need to modify A and B to incorporate the new In order to add the gradient norm constraints  this The dFor both approaches the implicit function is was assembled by 
   
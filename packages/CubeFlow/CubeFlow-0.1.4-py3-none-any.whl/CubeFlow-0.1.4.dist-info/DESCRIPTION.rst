CubeFlow
========

:abstract: CubeFlow is a Python framework to easily build and analyse grid based simulation such as heat transportation
    or fluid dynamics. CubeFlow aims to provide an easy implementation without the need of writing code other than
    the one needed for the actual simulation. CubeFlow is not a super fast simulator but focuses primarily on
    educational purposes.


Cube grid layout
----------------
.. image:: grid_image.png


Heat flow example
-----------------
Lets suppose we have a cube that is build of various materials and we want to explore the flow of heat within the
structure. We therefore define a quadratic grid that divides the cube in cells of homogeneous size. Each cell is
described by its coordinates, temperature (T) and thermal diffusivity (alpha). For the sake of simplicity we assume
that each cell is homogeneous regarding the distribution of its mass and density. The experiment at hand can then be
expressed in the form

.. math::
    \frac{\partial T(\vec{x},t)}{\partial t} & = &\alpha(\vec{x}) \triangle T(\vec{x}, t) \\
    \vec{x} \in \mathbb{R}^2, t \in \mathbb{R}^+, \alpha(\vec{x}) \in \mathbb{R}^+

in the continuity. We then use the grid to build a discrete model regarding space and time where c are a cells
coordinates and dt the time step of the simulation. We can then calculate the temperature delta
dT and the new temperature of the cell of simulation step i by using the discrete equation

.. math::
    \frac{dT(\vec{c}, t)_i}{dt} & = & \alpha(\vec{c}) \triangle T(\vec{c}, t)_i \\
    dT(\vec{c}, t)_i & = & dt \; \alpha(\vec{c}) \triangle T(\vec{c}, t)_i \\
    T_{i+1} &=& T_{i} + dT(\vec{c}, t)_i \\
    \vec{c} \in \mathbb{N}_0^2, \in \mathbb{Q}^+, \alpha(\vec{c}) \in \mathbb{Q}^+

Using cell coordinates m,n as positional reference instead of c the equation can be written as

.. math::
    dT_{m,n}^{(i)} &=& dt \; \alpha_{m,n} \triangle T_{m,n}^{(i)} \\
    T_{m,n}^{(i+1)} & = & T_{m,n}^{(i)} + dT_{m,n}^{(i)}

with the time index step written as "exponent". Note that this is not entirely correct if the alpha values of
the cells within differ, but we will ignore that for now and address this problem again in the error handling
chapter. We now have to discretise the Laplace operator which is done by
discretising the second derivate. We will use a discrete center derivation in this example, which leads to the
following equations regarding cell coordinates m,n and cell distances dx and dy:

.. math::
    f^{''}(x) &=& \frac{f(x+h) -2f(x)+f(x-h)}{h^2} \\
    \frac{\partial^2 T_{m,n}}{\partial x^2} & \approx & \frac{T_{m+1,n} - 2 T_{m,n} + T_{m-1,n}}{dx^2} \\
    \frac{\partial^2 T_{m,n}}{\partial y^2} & \approx & \frac{T_{m,n+1} - 2 T_{m,n} + T_{m,n-1}}{dy^2} \\
    dx = dy  &=&  dl \Rightarrow \\
    \frac{\partial^2 T_{m,n}}{\partial x^2} & \approx & \frac{T_{m+1,n} - 2 T_{m,n} + T_{m-1,n}}{dl^2} \\
    \frac{\partial^2 T_{m,n}}{\partial y^2} & \approx & \frac{T_{m,n+1} - 2 T_{m,n} + T_{m,n-1}}{dl^2} \\


Data types
----------
Now we need a data structure for the cells of our cube in order to simulate the heat flow. CubeFlow has some builtin
types to help simplifying the simulation process.

.. code-block:: python

    from typing import Dict, Sequence
    from cubeflow.cell import MetaCell, Scalar
    from cubeflow.report import Report
    from cubeflow.cube import CubeGrid

    class HeatCell(metaclass=MetaCell):
        temperature = Scalar()
        diffusivity = Scalar()
        flow = 0.0

By using MetaCell as metaclass we let CubeFlow take care of generating constructors and accessors.
The type Scalar used for temperature and diffusivity tell MetaCell that those fields are core values of the
simulation while flow is just used for storing a temporary value. We could define flow as Scalar, too if we want
to track its value over the time of the simulation. Scalar types behave like floats and are output of the various
reporting mechanisms of CubeFlow.

Simulation
----------

In almost every grid based simulation the border cells of the simulation domain have to be handled in a special way.
Since we want to explore the flow of heat within the cube we assume that the border cells will always have the same
temperature as the adjacent inner cell in order to prevent energy transport from or into the system.
We thus have two separate parts in our simulation, one regarding the borders and one regarding the inner cells.

Border handling
~~~~~~~~~~~~~~~
As each border cell should have at most one adjacent inner cell in CubeFlow, its following state is determined by
the mention adjacent cell alone. Depending of the type of the border, the calculation is more or less complex. In our
example we have the following equations that satisfy our conditions:

.. math::
    T_{0,y} &= &T_{1, y} \\
    T_{x_max+1,y} &= &T_{x_max, y} \\
    T_{x,0} &=& T_{x, 1} \\
    T_{x,y_max+1} &=& T_{x, y_max}


Inner cell handling
~~~~~~~~~~~~~~~~~~~
The first part of our handling of the inner cell  takes care of calculating the heat flow of each cell by applying
the Laplace operator regarding temperature to it while taking the thermal diffusivity into account. We will call this
step the **preparation step** in CubeFlow.
In the second part of the simulation we do the actual simulation, which means adding the calculated flow of each cell
to its temperature. This step is called **simulation step** within CubeFlow.

We will start by generating a data type that takes care of the simulation.

.. code-block:: python

    from cubeflow.simulator import BaseSimulator, add_derivations, border_handler

    @add_derivations
    class HeatSimulator(BaseSimulator[HeatCell]):
        Type = HeatCell

The *add_derivations* decorator adds methods for calculating the first and second derivation as well as the gradient
and laplace operator of each **HeatCell** member variable that is of type **Scalar**. We will now define a border
handler method for handling all borders of type 1, which means our mentioned now-flow borders.

.. code-block:: python

        @border_handler(1)
        def no_flow_border(self, cells: Dict[Sequence[int], HeatCell]) -> HeatCell:
            cell = cells[(0, 0)]
            adjacent = self._get_adjacent_inner(cells)
        if adjacent:
            # cell is not a corner
            cell.temperature = self._get_only_cell(adjacent)[1].temperature
            return cell
        else:
            return self._handle_corner(cells)

The **Dict[Sequence[int], HeatCell]** type represents a mapping window around the current cell which maps vectors
to neighbour cells. *cells[(0, 0)]* represents the inner cell, while *cell[(1, 0)]* represents the cell right to
cell. If such a cell does not exist, which is only possible for border cells, the corresponding value will be **None**.
Almost all functions dealing with cell will take **Dict[Sequence[int], HeatCell]** as argument.
**_get_adjacent_inner** returns all neighbour cells which are well defined (not **None**). If the second argument
to **get_adjacent_inner** is omitted or **True**, only cells along the direction of the grid axis are returned.
**_get_only_cell** is a helper function that returns the coordinates and cell of the only cell present in its argument.
The **border_handler(1)** call tells CubeFlow that this method takes care of every border of type 1 and will be called
if a border of type 1 is encountered during the handling of the border. We may define as much border handlers as we
wish for every positive integer, type 0 is reserved for inner cells, though. **handle_corner** is used for corner cells
that normally take no part of the simulation at all. For this reason, their values except their cell type are set to
any of the surrounding border cells, although ignoring them is fine, too.
The next function takes care of the **preparation step** in which we will calculate the heat flow of every cell. We
will do this by overwriting the **_prepare** method within our simulator class.

.. code-block:: python

        def _prepare(self, cells: Dict[Sequence[int], HeatCell]) -> HeatCell:
            cell = cells[(0, 0)]
            cell.flow = -cell.diffusivity * self.laplace_temperature(cells)
            return cell

The **_laplace_temperature** method has been added to our simulator class by the application of the **add_derivations**
decorator. A similar method **_laplace_diffusivity** exists although it is not used in our little example.
**_laplace_temperature** as well as all other methods regarding differentiation take additional parameters that modify
the way the summands of the denominator in the derivation equations are weighted. The default weights for the
**_laplace_diffusivity** methods represent the center differentiation method we chose early on.
The final method we will look at takes care of the actual simulation, the calculation of the cell's temperature.

.. code-block:: python

        def _simulate(self, cells: Dict[Sequence[int], HeatCell]) -> HeatCell:
            cell = cells[(0, 0)]
            cell.temperature += self.dt*cell.flow
            return cell

The **dt** member is the current time-step of our simulation, which is 0.1 time units per default and constant
throughout our simulation. A **t** member also exists, which represents the current time of our simulation.
The last thing we have to do is defining a small entry function for our program that loads a grid from file and
performs the actual simulation.

.. code-block:: python

    if __name__ == '__main__':
        from sys import argv
        from cubeflow.report.csv import CSVReport
        from cubeflow.predicates.counter import Counter
        simulator = HeatSimulator(CubeGrid.from_file(argv[1], HeatCell), [CSVReport('heat')])
        simulator.simulate_while(Counter(1000))

This will load a grid from command line and perform 1000 simulation steps, where each of them will be output to file
*heat.csv.i* where i ist the current step of the simulation. **simulate_while** takes a predicate that may evaluate
the grid and decide if another simulation step should take place. **Counter** of course does not do much evaluation.
The second argument of the **HeatSimulator** constructor takes a list of **Report** instances that will report every
simulation step. **CSVReport** for instance saves every step to a csv file for later analysis
(e.g. by the usage of *ParaView*).
Now we run out simulator with the sample grid provided in the Appendix of this document:

.. code-block:: bash

    python3 heat.py sample_heat_grid.json


Stability conditions
~~~~~~~~~~~~~~~~~~~~

Time-Step calculation
~~~~~~~~~~~~~~~~~~~~~

Creating grids
--------------

Appendix
--------

Sample heat grid
~~~~~~~~~~~~~~~~

.. include:: sample_heat_grid.json
    :code: json


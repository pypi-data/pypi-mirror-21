Revision History
================

Version 1.6.2: 2017-03-29
  * New: Cylindrical coordinate system can be requested by passing the optional parameter `coordinate_system="cylindrical"` to the lattice constructor.
  * New: `BesselState` class.
  * New: Optional Lee-Huang-Yang term in the Hamiltonian.
  * New: Calculate the azimuthal potential in the Hamiltonian.
  * Changed: The function `center_coordinates` was renamed to `map_lattice_to_coordinate_space`.
  * Changed: Hybrid kernel removed.
  * Changed: Improved the precision of energy expectation values.
  * Changed: The function `get_particle_density` no longer depends on the lattice resolution (see issues #161 and #124).
  * Fixed: 1D lattice works for all built-in state classes.
  * Fixed: Different resolution between the x- and y-axes works correctly in the CPU and GPU kernels.

Version 1.6.1: 2016-12-21
  * New: One-dimensional topology through the class `Lattice1D`.
  * New: The coordinate transformation and scaling is exposed via the function `center_coordinates`.
  * Changed: The two dimensional topology is now defined through the class `Lattice2D`.
  * Changed: The command-line interface was removed.
  * Changed: Python interface simplified and made more consistent.
  * Fixed: Different resolution and physical size across different axes is possible.
  * Fixed: Nonzero angular momentum no longer produces nan in the state if the offset is negative.

Version 1.5.5: 2016-06-13
  * Fixed: Particle density is scaled correctly.

Version 1.5.4: 2016-05-10
  * Fixed: `vortex_position` works correctly with Python 3.

Version 1.5.3: 2016-04-22
  * New: `vortex_position` function detects when a vortex is not present.

Version 1.5.2: 2016-03-02
  * New: Static library target to make distributed examples run easier on clusters.
  * Fixed: Windows version compiles again.
  * Fixed: Renormalization in the imaginary time evolution is fixed and simplified.
  * Fixed: Installing the C++ library works again.
  * Fixed: Python CUDA version works.

Version 1.5.1: 2016-02-15
  * New: Updating parameters is possible even after the solver was instantiated. Call the method `update_parameters` of the solver class.
  * New: Helper functions added to track vortices.
  * Changed: Since the lattice resolution is the same in either direction, now only one parameter handles it in the corresponding class.
  * Fixed: The second potential in a two-component Hamiltonian is correctly handled.

Version 1.5: 2016-01-31
  * New: Improved API that allows the user to define and solve problems in physical terms. Classes were introduced for the lattice, the state, the potential, the Hamiltonian, and for the solver.
  * New: Time-dependent potentials are possible.
  * New: CUDA support in the Python interface.
  * Changed: SSE kernel was removed.
  * Changed: MATLAB interface was removed.
  * Changed: More robust compilation of CUDA version in the Python wrapper.
  * Fixed: Code compiles again with the hybrid kernel.

Version 1.4: 2015-10-25
  * New: CPU kernel implements the Gross-Pitaevskii equation.
  * New: performing imaginary time evolution, all kernels output a wave function normalized with a set value provided as input.
  * New: The command-line interface, and the Python and MATLAB wrappers only need Hamiltonian parameters, lattice parameters and evolution parameters as input.
  * New: Sphinx documentation for the Python wrapper, including examples.
  * Changed: Example of MATLAB wrapper.
  * Fixed: Python 3 compatibility.
  * Fixed: MAC OS X can compile, but it does not support SSE kernel.

Version 1.3: 2015-07-04
  * New: Wrappers for Python and MATLAB.
  * New: Compiles on Windows with Visual Studio.
  * Changed: Code compiles without MPI.
  * Fixed: No single process has to hold the entire state or potential in memory.

Version 1.2: 2015-06-08
  * New: Imaginary time evolution to find ground state.
  * New: Periodic boundary conditions are possible.
  * New: Arbitrary stationary potential function can be defined.
  * New: CLI for specifying the files of the initial state and the potential, and the parameters of the Hamiltonian.
  * New: API added through the `trotter` function.
  * New: Convenience function to get expectation values (`expect_values`).
  * New: Unit testing framework.
  * Changed: Single-precision calculations were removed entirely.
  * Changed: Examples split into separate folder.
  * Changed: Better testing of MPI dependencies by configure script.
  * Changed: Improved treatment of Intel compilers.

Version 1.1: 2014-06-12
  * New: Build system revised, CUDA is no longer necessary.

Version 1.0: 2012-06-28
  * Initial release.

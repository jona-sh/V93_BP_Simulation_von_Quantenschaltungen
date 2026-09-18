.. q_simulator documentation master file, created by
   sphinx-quickstart on Wed Sep 16 16:05:52 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

q_simulator documentation
=========================

``q_simulator`` is an educational quantum-circuit simulator. It accepts
Qiskit circuits and returns a statevector as well as measurement counts of the simulation.

Available simulation methods are:

* ``default``: Qiskit Aer backend.
* ``einsum``: NumPy tensor operations.
* ``loop``: Explicit Python loops.
* ``numba``: Numba-compiled loops.

As you can see, our simulation performs much better than the Qiskit Aer backend. The screenshot below shows the performance of our simulation compared to the Qiskit Aer backend.

.. figure:: _static/simulation_performance.png
   :alt: Documentation screenshot
   :align: center

   Simulation speed of the different methods with varying circuit sizes. The qiskiit Aer backend is denoted as default.


.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   api
   tutorial-guide

API Reference
=============

The public API is re-exported from :mod:`q_simulator`. The entries below are
generated directly from the source docstrings.

.. contents:: Simulation API
   :local:
   :depth: 2

.. automodule:: q_simulator
   :members:
   :show-inheritance:

Simulation functions
--------------------

.. automodule:: q_simulator.simulate
   :members: simulate
   :show-inheritance:

Simulation helpers
------------------

.. automodule:: q_simulator.simulate
   :members: _simulate_default, _simulate_einsum, _simulate_loop, _simulate_numba
   :show-inheritance:

Gate Application Functions
------------------

.. automodule:: q_simulator.simulate
   :members: _apply_unitary, _apply_cx_einsum, _apply_unitary_loop, _apply_cx_loop, _apply_unitary_numba, _apply_cx_numba
   :show-inheritance:

Data objects
------------

.. automodule:: q_simulator.objects
   :members: Configuration, Result
   :show-inheritance:

Gate objects
------------

.. automodule:: q_simulator.objects
   :members: X, Y, Z, H, S, CX
   :show-inheritance:

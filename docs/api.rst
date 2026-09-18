API Reference
=============

The public API is re-exported from :mod:`q_simulator_bp_feljon`. The entries below are
generated directly from the source docstrings.

.. contents:: Simulation API
   :local:
   :depth: 2

.. automodule:: q_simulator_bp_feljon
   :members:
   :show-inheritance:

Simulation functions
--------------------

.. automodule:: q_simulator_bp_feljon.simulate
   :members: simulate
   :noindex:
   :show-inheritance:

Simulation helpers
------------------

.. automodule:: q_simulator_bp_feljon.simulate
   :members: _simulate_default, _simulate_einsum, _simulate_loop, _simulate_numba
   :noindex:
   :show-inheritance:

Gate Application Functions
--------------------------

.. automodule:: q_simulator_bp_feljon.simulate
   :members: _apply_unitary, _apply_cx_einsum, _apply_unitary_loop, _apply_cx_loop, _apply_unitary_numba, _apply_cx_numba
   :noindex:
   :show-inheritance:

Data objects
------------

.. automodule:: q_simulator_bp_feljon.objects
   :members: Configuration, Result
   :noindex:
   :show-inheritance:

Gate objects
------------

.. automodule:: q_simulator_bp_feljon.objects
   :members: X, Y, Z, H, S, CX
   :noindex:
   :show-inheritance:

# import numpy as np
# import pytest
# from qiskit import QuantumCircuit
# from qiskit.quantum_info import Statevector
# from qiskit_aer import AerSimulator

# import q_simulator as qs


# def test_einsum_single():
#     N = 5
#     psi = np.array([1] + [0] * (2**N - 1), dtype=complex)
#     result = qs._apply_single_qubit_gate(psi, qs.H, 2)

"""Data containers and standard quantum-gate matrices."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Configuration:
    """Configure a simulation run.

    Attributes:
        method: Simulation backend, either ``"default"`` or ``"einsum"``.
        number_of_shots: Number of measurement shots requested.
    """

    method: str = "default"
    number_of_shots: int = 2**16


class Result:
    """Store the outcome of a quantum-circuit simulation.

    Attributes:
        counts: Measurement probabilities or shot counts keyed by bitstring.
        statevector: Final state vector of the simulated circuit.
    """

    def __init__(self, counts: dict, statevector: np.ndarray):
        self.counts = counts
        self.statevector = statevector


H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
"""The Hadamard gate matrix."""

X = np.array([[0, 1], [1, 0]])
"""The Pauli-X gate matrix."""
Y = np.array([[0, -1j], [1j, 0]])
"""The Pauli-Y gate matrix."""
Z = np.array([[1, 0], [0, -1]])
"""The Pauli-Z gate matrix."""
S = np.array([[1, 0], [0, 1j]])
"""The S gate matrix."""
CX = np.zeros((2,) * 4)
"""The CNOT gate matrix in tensor notation."""
CX[0, 0, 0, 0] = 1
CX[0, 1, 0, 1] = 1
CX[1, 0, 1, 1] = 1
CX[1, 1, 1, 0] = 1

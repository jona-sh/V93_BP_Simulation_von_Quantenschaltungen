"""Data containers and standard quantum-gate matrices."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Configuration:
    """Configure a simulation run.

    :param method: Simulation backend, either ``"default"`` or ``"einsum"``.
    :param number_of_shots: Number of measurement shots requested.
    """

    method: str = "default"
    number_of_shots: int = 2**16


class Result:
    """Store the outcome of a quantum-circuit simulation.

    :param counts: Measurement probabilities or shot counts keyed by bitstring.
    :param statevector: Final state vector of the simulated circuit.
    """

    def __init__(self, counts: dict, statevector: np.ndarray):
        self.counts = counts
        self.statevector = statevector


H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
S = np.array([[1, 0], [0, 1j]])
CX = np.zeros((2,) * 4)
CX[0, 0, 0, 0] = 1
CX[0, 1, 0, 1] = 1
CX[1, 0, 1, 1] = 1
CX[1, 1, 1, 0] = 1

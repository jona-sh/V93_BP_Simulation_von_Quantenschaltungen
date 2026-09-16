import numpy as np
from qiskit import QuantumCircuit

from .objects import Configuration, Result


def simulate(qc: QuantumCircuit, config: Configuration) -> Result:
    print("test")
    return Result(counts={}, statevector=np.array([0, 1], dtype=complex))

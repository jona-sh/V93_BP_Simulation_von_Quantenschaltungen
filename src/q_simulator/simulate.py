import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from .objects import Configuration, Result


def simulate(qc: QuantumCircuit, config: Configuration) -> Result:
    match config.method:
        case "default":
            return _simulate_default(qc, config)
        case "einsum":
            return _simulate_einsum(qc, config)
        case _:
            raise ValueError(f"Unknown simulation method: {config.method}")


def _simulate_default(qc: QuantumCircuit, config: Configuration) -> Result:

    qc_to_run = qc.copy()
    qc_to_run.save_statevector()

    backend = AerSimulator()
    result = backend.run(qc_to_run, shots=config.number_of_shots).result()
    counts = result.get_counts(qc_to_run)
    statevector = np.asarray(result.get_statevector(qc_to_run))

    return Result(counts=counts, statevector=statevector)


def _simulate_einsum(qc: QuantumCircuit, config: Configuration) -> Result:
    _apply_unitary(np.array([]), np.array([]), 0)
    _apply_cx_einsum(np.array([]), 0, 1)
    return Result(counts={}, statevector=np.array([]))


def _apply_unitary(
    statevector: np.ndarray, operator: np.ndarray, qubit: int
) -> np.ndarray:
    return np.array([])


def _apply_cx_einsum(statevector: np.ndarray, control: int, target: int) -> np.ndarray:
    return np.array([])

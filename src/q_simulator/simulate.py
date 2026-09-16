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
    N = int(np.log2(len(statevector)))
    assert 0 <= qubit < N, "qubit index out of range"
    psi = np.reshape(statevector, (2,) * N, order="F")
    s = "bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s[:N]
    I = s[qubit]
    to = s[:qubit] + "a" + s[qubit + 1 : N]
    psi_new = np.einsum(f"a{I},{s[:N]}->{to}", operator, psi)
    return np.reshape(psi_new, -1, order="F")


def _apply_cx_einsum(statevector: np.ndarray, control: int, target: int) -> np.ndarray:
    i, j = control, target
    N = len(statevector.shape)

    assert 0 <= control < N, "qubit index out of range"
    assert 0 <= target < N, "qubit index out of range"
    assert control != target, "control and target qubits must be different"

    cx = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    cx = np.reshape(cx, (2,) * 4, order="F")

    s = "cdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s[:N]
    I = s[i]
    J = s[j]
    if i < j:
        to = s[:i] + "a" + s[i + 1 : j] + "b" + s[j + 1 : N]
    else:
        to = s[:j] + "b" + s[j + 1 : i] + "a" + s[i + 1 : N]
    psi_new = np.einsum(f"ab{I}{J},{s[:N]}->{to}", cx, statevector)
    return psi_new

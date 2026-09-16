import numpy as np
from qiskit import QuantumCircuit, transpile
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
    ns = config.number_of_shots
    transpiled_qc = transpile(qc, optimization_level=0, basis_gates=["u3", "cx"])
    num_qubits = transpiled_qc.num_qubits
    statevector = np.zeros(2**num_qubits, dtype=complex)
    state = np.reshape(statevector, (2,) * num_qubits, order="F")

    for instr in transpiled_qc.data:
        # print(123476,instr)
        name = instr.operation.name
        qubits = [q for q in instr.qubits]
        if name == "u":
            matrix = instr.operation.to_matrix()
            state = _apply_unitary(state, matrix, qubits[0])
        elif name == "cx":
            state = _apply_cx_einsum(state, qubits[0], qubits[1])
        elif name == "measure" or name == "barrier":
            pass
        else:
            raise ValueError(f"Unsupported gate: {name}")

    final_statevector = np.reshape(state, -1, order="F")
    countslist = np.abs(final_statevector) ** 2
    countslist = np.round(countslist * ns).astype(int)
    counts = {}
    for i, count in enumerate(countslist):
        if count > 0:
            counts[f"{i:0{transpiled_qc.num_qubits}b}"] = count

    return Result(counts=counts, statevector=final_statevector)


def _apply_unitary(
    statevector: np.ndarray, operator: np.ndarray, qubit: int
) -> np.ndarray:
    N = len(statevector.shape)
    assert 0 <= qubit < N, "qubit index out of range"
    s = "bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s[:N]
    I = s[qubit]
    to = s[:qubit] + "a" + s[qubit + 1 : N]
    psi_new = np.einsum(f"a{I},{s[:N]}->{to}", operator, statevector)
    return psi_new


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

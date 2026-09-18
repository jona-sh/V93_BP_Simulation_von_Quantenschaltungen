"""Simulation backends and tensor-network gate operations."""

import numpy as np
from numba import njit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from .objects import CX, Configuration, Result


def simulate(qc: QuantumCircuit, config: Configuration) -> Result:
    """Simulate a Qiskit quantum circuit.

    Args:
        qc: Qiskit Quantum Circuit Object to execute.
        config: Simulation configuration. Object of type ``Configuration`` containing the simulation method and number of shots.

    Returns:
        Simulation results. Object of type ``Result`` containing the measurement counts and the final statevector.

    Raises:
        ValueError: If ``config.method`` is not supported.
    """

    match config.method:
        case "default":
            return _simulate_default(qc, config)
        case "einsum":
            return _simulate_einsum(qc, config)
        case "loop":
            return _simulate_loop(qc, config)
        case "numba":
            return _simulate_numba(qc, config)
        case _:
            raise ValueError(f"Unknown simulation method: {config.method}")


def _simulate_default(qc: QuantumCircuit, config: Configuration) -> Result:
    """Simulate a Qiskit quantum circuit using the default AerSimulator backend.

    Args:
        qc: Qiskit Quantum Circuit Object to execute.
        config: Simulation configuration. Object of type ``Configuration`` containing the simulation method and number of shots.

    Returns:
        Simulation results. Object of type ``Result`` containing the measurement counts and the final statevector.
    """
    qc_to_run = qc.copy()
    qc_to_run.save_statevector()
    backend = AerSimulator(
        fusion_enable=False, max_parallel_threads=1
    )  # to avoid race conditions in parallel execution
    qc_to_run = transpile(qc_to_run, backend)
    result = backend.run(qc_to_run, shots=config.number_of_shots).result()
    counts = result.get_counts(qc_to_run)
    statevector = np.asarray(result.get_statevector(qc_to_run))

    return Result(counts=counts, statevector=statevector)


def _simulate_einsum(qc: QuantumCircuit, config: Configuration) -> Result:
    """Simulate a Qiskit quantum circuit using the einsum-based tensor-network implementation.

    Args:
        qc: Qiskit Quantum Circuit Object to execute.
        config: Simulation configuration. Object of type ``Configuration`` containing the simulation method and number of shots.

    Returns:
        Simulation results. Object of type ``Result`` containing the measurement counts and the final statevector.
    """
    transpiled_qc = transpile(qc, optimization_level=0, basis_gates=["u3", "cx"])
    num_qubits = transpiled_qc.num_qubits
    statevector = np.zeros(2**num_qubits, dtype=complex)
    statevector[0] = 1
    state = np.reshape(statevector, (2,) * num_qubits, order="F")

    for instr in transpiled_qc.data:
        name = instr.operation.name
        qubits = [transpiled_qc.find_bit(q).index for q in instr.qubits]
        if name in {"u", "u3"}:
            matrix = instr.operation.to_matrix()
            state = _apply_unitary(state, matrix, qubits[0])
        elif name == "cx":
            state = _apply_cx_einsum(state, qubits[0], qubits[1])
        elif name == "measure" or name == "barrier":
            pass
        else:
            raise ValueError(f"Unsupported gate: {name}")

    final_statevector = np.reshape(state, -1, order="F")
    probabilities = np.abs(final_statevector) ** 2
    counts = {}
    for i, probability in enumerate(probabilities):
        if probability > 0:
            counts[f"{i:0{transpiled_qc.num_qubits}b}"] = probability

    return Result(counts=counts, statevector=final_statevector)


def _simulate_loop(qc: QuantumCircuit, config: Configuration) -> Result:
    """Simulate a Qiskit quantum circuit using the fast loop implementation.

    Args:
        qc: Qiskit Quantum Circuit Object to execute.
        config: Simulation configuration. Object of type ``Configuration`` containing the simulation method and number of shots.

    Returns:
        Simulation results. Object of type ``Result`` containing the measurement counts and the final statevector.
    """
    transpiled_qc = transpile(qc, optimization_level=0, basis_gates=["u3", "cx"])
    num_qubits = transpiled_qc.num_qubits
    statevector = np.zeros(2**num_qubits, dtype=complex)
    statevector[0] = 1
    state = statevector

    for instr in transpiled_qc.data:
        name = instr.operation.name
        qubits = [transpiled_qc.find_bit(q).index for q in instr.qubits]
        if name in {"u", "u3"}:
            matrix = instr.operation.to_matrix()
            state = _apply_unitary_loop(state, matrix, qubits[0])
        elif name == "cx":
            state = _apply_cx_loop(state, qubits[0], qubits[1])
        elif name == "measure" or name == "barrier":
            pass
        else:
            raise ValueError(f"Unsupported gate: {name}")

    final_statevector = state
    probabilities = np.abs(final_statevector) ** 2
    counts = {}
    for i, probability in enumerate(probabilities):
        if probability > 0:
            counts[f"{i:0{transpiled_qc.num_qubits}b}"] = probability

    return Result(counts=counts, statevector=final_statevector)


def _simulate_numba(qc: QuantumCircuit, config: Configuration) -> Result:
    """Simulate a Qiskit quantum circuit using the numba-accelerated fast loop implementation.

    Args:
        qc: Qiskit Quantum Circuit Object to execute.
        config: Simulation configuration. Object of type ``Configuration`` containing the simulation method and number of shots.

    Returns:
        Simulation results. Object of type ``Result`` containing the measurement counts and the final statevector.
    """
    transpiled_qc = transpile(qc, optimization_level=0, basis_gates=["u3", "cx"])
    num_qubits = transpiled_qc.num_qubits
    statevector = np.zeros(2**num_qubits, dtype=complex)
    statevector[0] = 1
    state = statevector

    for instr in transpiled_qc.data:
        name = instr.operation.name
        qubits = [transpiled_qc.find_bit(q).index for q in instr.qubits]
        if name in {"u", "u3"}:
            matrix = instr.operation.to_matrix()
            state = _apply_unitary_numba(state, matrix, qubits[0])
        elif name == "cx":
            state = _apply_cx_numba(state, qubits[0], qubits[1])
        elif name == "measure" or name == "barrier":
            pass
        else:
            raise ValueError(f"Unsupported gate: {name}")

    final_statevector = state
    probabilities = np.abs(final_statevector) ** 2
    counts = {}
    for i, probability in enumerate(probabilities):
        if probability > 0:
            counts[f"{i:0{transpiled_qc.num_qubits}b}"] = probability

    return Result(counts=counts, statevector=final_statevector)


def _apply_unitary(
    statevector: np.ndarray, operator: np.ndarray, qubit: int
) -> np.ndarray:
    """Apply a single-qubit unitary operator to a specific qubit in the statevector using einsum.

    Args:
        statevector: The current statevector of the quantum system as a tensor.
        operator: The unitary operator to apply.
        qubit: The index of the qubit to apply the operator to.

    Returns:
        The updated statevector after applying the operator as a tensor.
    """
    N = len(statevector.shape)
    assert 0 <= qubit < N, "qubit index out of range"
    s = "bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    I = s[qubit]
    to = s[:qubit] + "a" + s[qubit + 1 : N]
    psi_new = np.einsum(f"a{I},{s[:N]}->{to}", operator, statevector)
    return psi_new


def _apply_cx_einsum(statevector: np.ndarray, control: int, target: int) -> np.ndarray:
    """Apply a CNOT gate to the statevector using einsum.

    Args:
        statevector: The current statevector of the quantum system as a tensor.
        control: The index of the control qubit.
        target: The index of the target qubit.

    Returns:
        The updated statevector after applying the CNOT gate  as a tensor.
    """
    i, j = control, target
    N = len(statevector.shape)

    assert 0 <= control < N, "qubit index out of range"
    assert 0 <= target < N, "qubit index out of range"
    assert control != target, "control and target qubits must be different"

    s = "cdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    I = s[i]
    J = s[j]
    if i < j:
        to = s[:i] + "a" + s[i + 1 : j] + "b" + s[j + 1 : N]
    else:
        to = s[:j] + "b" + s[j + 1 : i] + "a" + s[i + 1 : N]
    psi_new = np.einsum(f"ab{I}{J},{s[:N]}->{to}", CX, statevector)
    return psi_new


def _apply_unitary_loop(
    statevector: np.ndarray, operator: np.ndarray, qubit: int
) -> np.ndarray:
    """Apply a single-qubit unitary operator to a specific qubit in the statevector using the fast loop method.

    Args:
        statevector: The current statevector of the quantum system as a tensor.
        operator: The unitary operator to apply.
        qubit: The index of the qubit to apply the operator to.

    Returns:
        The updated statevector after applying the operator as a tensor.
    """
    N = int(np.log2(statevector.size))
    assert 0 <= qubit < N, "qubit index out of range"

    for r in range(2**qubit):
        for s in range(2 ** (N - qubit - 1)):
            index = r + s * 2 ** (qubit + 1)
            partner = index + 2**qubit

            statevector_index = statevector[index]
            statevector[index] = (
                operator[0, 0] * statevector_index
                + operator[0, 1] * statevector[partner]
            )
            statevector[partner] = (
                operator[1, 0] * statevector_index
                + operator[1, 1] * statevector[partner]
            )
    return statevector


def _apply_cx_loop(statevector: np.ndarray, control: int, target: int) -> np.ndarray:
    """Apply a CNOT gate to the statevector using the fast loop method.

    Args:
        statevector: The current statevector of the quantum system as a tensor.
        control: The index of the control qubit.
        target: The index of the target qubit.

    Returns:
        The updated statevector after applying the CNOT gate  as a tensor.
    """
    N = int(np.log2(statevector.size))

    assert 0 <= control < N, "qubit index out of range"
    assert 0 <= target < N, "qubit index out of range"
    assert control != target, "control and target qubits must be different"

    for r in range(2**target):
        for s in range(2 ** (N - target - 1)):
            index = r + s * 2 ** (target + 1)
            partner = index + 2**target
            if (index >> control) & 1:
                temp = statevector[index]
                statevector[index] = statevector[partner]
                statevector[partner] = temp
    return statevector


@njit
def _apply_unitary_numba(
    statevector: np.ndarray, operator: np.ndarray, qubit: int
) -> np.ndarray:
    """Apply a single-qubit unitary operator to a specific qubit in the statevector using the fast loop method with numba speedup.

    Args:
        statevector: The current statevector of the quantum system as a vector.
        operator: The unitary operator to apply.
        qubit: The index of the qubit to apply the operator to.

    Returns:
        The updated statevector after applying the operator as a vector.
    """
    N = int(np.log2(statevector.size))
    assert 0 <= qubit < N, "qubit index out of range"

    for r in range(2**qubit):
        for s in range(2 ** (N - qubit - 1)):
            index = r + s * 2 ** (qubit + 1)
            partner = index + 2**qubit

            statevector_index = statevector[index]
            statevector[index] = (
                operator[0, 0] * statevector_index
                + operator[0, 1] * statevector[partner]
            )
            statevector[partner] = (
                operator[1, 0] * statevector_index
                + operator[1, 1] * statevector[partner]
            )
    return statevector


@njit
def _apply_cx_numba(statevector: np.ndarray, control: int, target: int) -> np.ndarray:
    """Apply a CNOT gate to the statevector using the fast loop method with numba speedup.

    Args:
        statevector: The current statevector of the quantum system as a vector.
        control: The index of the control qubit.
        target: The index of the target qubit.

    Returns:
        The updated statevector after applying the CNOT gate  as a vector.
    """
    N = int(np.log2(statevector.size))

    assert 0 <= control < N, "qubit index out of range"
    assert 0 <= target < N, "qubit index out of range"
    assert control != target, "control and target qubits must be different"

    for r in range(2**target):
        for s in range(2 ** (N - target - 1)):
            index = r + s * 2 ** (target + 1)
            partner = index + 2**target
            if (index >> control) & 1:
                temp = statevector[index]
                statevector[index] = statevector[partner]
                statevector[partner] = temp
    return statevector

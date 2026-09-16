import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from .objects import Configuration, Result


def simulate(qc: QuantumCircuit, config: Configuration) -> Result:
    if config.method != "aer_simulator":
        raise ValueError("Unsupported simulation method")

    qc_to_run = qc.copy()
    qc_to_run.save_statevector()

    backend = AerSimulator()
    result = backend.run(qc_to_run, shots=config.number_of_shots).result()
    counts = result.get_counts(qc_to_run)
    statevector = np.asarray(result.get_statevector(qc_to_run))

    return Result(counts=counts, statevector=statevector)

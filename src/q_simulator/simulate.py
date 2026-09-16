# import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from .objects import Configuration, Result


def simulate(qc: QuantumCircuit, config: Configuration) -> Result:
    match config.method:
        case "default":
            return _simulate_default(qc, config)
        case _:
            raise ValueError(f"Unknown simulation method: {config.method}")


def _simulate_default(qc: QuantumCircuit, config: Configuration) -> Result:
    qc.remove_final_measurements()
    statevector = Statevector.from_instruction(qc)
    qc.measure_all()
    aer_sim = AerSimulator(shots=config.number_of_shots)
    result = aer_sim.run(qc).result()
    return Result(counts=result.get_counts(), statevector=statevector.data)

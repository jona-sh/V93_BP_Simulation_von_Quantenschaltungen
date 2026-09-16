import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

import q_simulator as qs


def test_simulate_default_1():
    qc = QuantumCircuit(4)
    qc.h([0, 1, 2, 3])
    ns = 2**16

    conf = qs.Configuration(method="default", number_of_shots=ns)
    result = qs.simulate(qc.copy(), conf)

    statevector = Statevector.from_instruction(qc)

    qc.measure_all()

    aer_sim = AerSimulator(shots=ns)
    result_tmp = aer_sim.run(qc).result()
    result_aer = qs.Result(counts=result_tmp.get_counts(), statevector=statevector.data)
    assert isinstance(result_aer, qs.Result)
    assert np.allclose(result_aer.statevector, result.statevector)
    # assert result_aer.counts == result.counts


@pytest.mark.parametrize("seed", [1, 2, 3, 42, 1234])
def test_random_circuit(seed):
    qc = QuantumCircuit(3)
    ns = 2**16
    rng = np.random.default_rng(seed)
    for _ in range(10):
        gate = rng.choice(["h", "x", "y", "z", "cx"])
        if gate == "cx":
            control, target = rng.choice(range(3), size=2, replace=False)
            qc.cx(control, target)
        else:
            qubit = rng.choice(range(3))
            getattr(qc, gate)(qubit)
    conf = qs.Configuration(method="default", number_of_shots=ns)
    result = qs.simulate(qc.copy(), conf)

    statevector = Statevector.from_instruction(qc)

    qc.measure_all()

    aer_sim = AerSimulator(shots=ns)
    result_tmp = aer_sim.run(qc).result()
    result_aer = qs.Result(counts=result_tmp.get_counts(), statevector=statevector.data)
    assert isinstance(result_aer, qs.Result)
    assert np.allclose(result_aer.statevector, result.statevector)

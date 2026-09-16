import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

import q_simulator as qs


def test_simulate_default_1():
    tol = 15
    qc = QuantumCircuit(4)
    qc.h([0, 1, 2, 3])
    ns = 2**16

    conf = qs.Configuration(method="default", number_of_shots=ns)
    result = qs.simulate(qc.copy(), conf)

    statevector = Statevector.from_instruction(qc)

    qc.measure_all()

    aer_sim = AerSimulator()
    result_cnt = aer_sim.run(qc, shots=ns).result().get_counts()
    result_aer = qs.Result(counts=result_cnt, statevector=statevector.data)
    assert isinstance(result_aer, qs.Result)
    assert np.allclose(result_aer.statevector, result.statevector)

    for k, v in result_aer.counts.items():
        assert k in result.counts
        assert abs(result.counts[k] * ns - v) < tol


@pytest.mark.parametrize("seed", [1, 2, 3, 42, 1234])
def test_random_circuit(seed):
    tol = 15
    qc = QuantumCircuit(3)
    rng = np.random.default_rng(seed)
    for _ in range(10):
        gate = rng.choice(["h", "x", "y", "z", "cx"])
        if gate == "cx":
            control, target = rng.choice(range(3), size=2, replace=False)
            qc.cx(control, target)
        else:
            qubit = rng.choice(range(3))
            getattr(qc, gate)(qubit)
    ns = 2**16

    conf = qs.Configuration(method="default", number_of_shots=ns)
    result = qs.simulate(qc.copy(), conf)

    statevector = Statevector.from_instruction(qc)

    qc.measure_all()

    aer_sim = AerSimulator()
    result_cnt = aer_sim.run(qc, shots=ns).result().get_counts()
    result_aer = qs.Result(counts=result_cnt, statevector=statevector.data)
    assert isinstance(result_aer, qs.Result)
    assert np.allclose(result_aer.statevector, result.statevector)

    for k, v in result_aer.counts.items():
        assert k in result.counts
        assert abs(result.counts[k] * ns - v) < tol

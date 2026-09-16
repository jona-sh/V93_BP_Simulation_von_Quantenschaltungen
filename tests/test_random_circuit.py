import numpy as np
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
    print(result.counts)
    print(result_aer.counts)
    for k, v in result_aer.counts.items():
        assert k in result.counts
        assert abs(result.counts[k] * ns - v) < tol

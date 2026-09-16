import numpy as np
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


test_simulate_default_1()

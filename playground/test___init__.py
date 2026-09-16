import numpy as np
from qiskit import QuantumCircuit

import q_simulator as qs

testcircuit = QuantumCircuit(2)
testcircuit.measure_all()

result = qs.simulate(
    testcircuit,
    qs.Configuration(method="aer_simulator", number_of_shots=1024),
)

assert isinstance(result.counts, dict)
assert isinstance(result.statevector, np.ndarray)
assert result.statevector.shape == (4,)

print(result.counts, result.statevector)

"""Time all simulator methods on the test circuit."""

import time

from qiskit.circuit.random import random_circuit

import q_simulator as qs

circuit = random_circuit(18, 50)
circuit.draw()
config = qs.Configuration(number_of_shots=2**16)

for method in ["default", "einsum", "loop", "numba"]:
    config.method = method
    start = time.time()
    qs.simulate(circuit.copy(), config)
    elapsed = time.time() - start
    print(f"{method:>7}: {elapsed:.6f} s")

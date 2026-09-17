"""Time all simulator methods on the test circuit."""

import time

from qiskit.circuit.random import random_circuit

import q_simulator as qs

# def build_test_circuit() -> QuantumCircuit:
#     circuit = random_circuit(5, 5)
#     # rng = np.random.default_rng(1)
#     # for _ in range(10):
#     #     gate = rng.choice(["h", "x", "y", "z", "cx"])
#     #     if gate == "cx":
#     #         control, target = rng.choice(3, size=2, replace=False)
#     #         circuit.cx(control, target)
#     #     else:
#     #         getattr(circuit, gate)(rng.choice(3))
#     return circuit


circuit = random_circuit(14, 100)
circuit.draw()
config = qs.Configuration(number_of_shots=2**16)

for method in ["default", "einsum", "loop", "numba"]:
    config.method = method
    start = time.time()
    qs.simulate(circuit.copy(), config)
    elapsed = time.time() - start
    print(f"{method:>7}: {elapsed:.6f} s")

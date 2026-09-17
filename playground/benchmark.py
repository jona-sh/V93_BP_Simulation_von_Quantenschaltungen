"""Time all simulator methods on the test circuit."""

import time

import matplotlib.pyplot as plt
from qiskit.circuit.random import random_circuit

import q_simulator as qs

data_qubits: dict[str, list[float]] = {
    "default": [],
    "einsum": [],
    "loop": [],
    "numba": [],
}
data_depths: dict[str, list[float]] = {
    "default": [],
    "einsum": [],
    "loop": [],
    "numba": [],
}
qubits_iterate = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
depths_iterate = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

for qubits in qubits_iterate:
    print(f"Simulating circuit with {qubits} qubits and depth 50")
    circuit = random_circuit(qubits, 50)
    circuit.draw()
    config = qs.Configuration(number_of_shots=2**16)
    for method in ["default", "einsum", "loop", "numba"]:
        config.method = method
        start = time.time()
        qs.simulate(circuit.copy(), config)
        elapsed = time.time() - start
        data_qubits[method].append(elapsed)
        print(f"{method:>7}: {elapsed:.6f} s")

for depth in depths_iterate:
    print(f"Simulating circuit with 15 qubits and depth {depth}")
    circuit = random_circuit(10, depth)
    circuit.draw()
    config = qs.Configuration(number_of_shots=2**16)
    for method in ["default", "einsum", "loop", "numba"]:
        config.method = method
        start = time.time()
        qs.simulate(circuit.copy(), config)
        elapsed = time.time() - start
        data_depths[method].append(elapsed)
        print(f"{method:>7}: {elapsed:.6f} s")

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(data_qubits["default"], label="default")
plt.plot(data_qubits["einsum"], label="einsum")
plt.plot(data_qubits["loop"], label="loop")
plt.plot(data_qubits["numba"], label="numba")
plt.xlabel("Qubits")
plt.ylabel("Time (s)")
plt.title("Performance Comparison")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(data_depths["default"], label="default")
plt.plot(data_depths["einsum"], label="einsum")
plt.plot(data_depths["loop"], label="loop")
plt.plot(data_depths["numba"], label="numba")
plt.xlabel("Depth")
plt.ylabel("Time (s)")
plt.title("Performance Comparison")
plt.legend()


plt.show()  # savefig('simulation_performance.png')

"""Time all simulator methods on the test circuit."""

import time
from pathlib import Path

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
qubits_iterate = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20]
depths_iterate = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 750]

for qubits in qubits_iterate:
    print(f"Simulating circuit with {qubits} qubits and depth 50")
    circuit = random_circuit(qubits, 50)
    # circuit.draw()
    config = qs.Configuration(number_of_shots=2**16)
    for method in ["default", "einsum", "loop", "numba"]:
        if method == "loop" and qubits >= 13:
            continue
        if method == "einsum" and qubits >= 17:
            continue
        config.method = method
        start = time.time()
        qs.simulate(circuit.copy(), config)
        elapsed = time.time() - start
        data_qubits[method].append(elapsed)
        print(f"{method:>7}: {elapsed:.6f} s")

for depth in depths_iterate:
    print(f"Simulating circuit with 15 qubits and depth {depth}")
    circuit = random_circuit(10, depth)
    # circuit.draw()
    config = qs.Configuration(number_of_shots=2**16)
    for method in ["default", "einsum", "loop", "numba"]:
        if method == "einsum" and depth > 600:
            continue
        if method == "loop" and depth > 400:
            continue
        config.method = method
        start = time.time()
        qs.simulate(circuit.copy(), config)
        elapsed = time.time() - start
        data_depths[method].append(elapsed)
        print(f"{method:>7}: {elapsed:.6f} s")

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(qubits_iterate, data_qubits["default"], label="default")
plt.plot([q for q in qubits_iterate if q < 17], data_qubits["einsum"], label="einsum")
plt.plot([q for q in qubits_iterate if q < 13], data_qubits["loop"], label="loop")
plt.plot(qubits_iterate, data_qubits["numba"], label="numba")
plt.xlabel("Qubits")
plt.ylabel("Time (s)")
plt.semilogy()
plt.title("Performance Comparison")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(depths_iterate, data_depths["default"], label="default")
plt.plot([d for d in depths_iterate if d <= 600], data_depths["einsum"], label="einsum")
plt.plot([d for d in depths_iterate if d <= 400], data_depths["loop"], label="loop")
plt.plot(depths_iterate, data_depths["numba"], label="numba")
plt.xlabel("Depth")
plt.ylabel("Time (s)")
plt.semilogy()
plt.title("Performance Comparison")
plt.legend()

benchmark_dir = Path(__file__).resolve().parent
plot_path = benchmark_dir / "simulation_performance.png"
plt.savefig(plot_path, dpi=200)

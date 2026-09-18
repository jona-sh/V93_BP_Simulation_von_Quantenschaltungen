# q_simulator

`q_simulator` is an educational quantum-circuit simulator developed for the
University of Stuttgart practical course *Simulation von Quantenschaltungen*.
It accepts Qiskit `QuantumCircuit` objects and returns the resulting
statevector together with measurement probabilities or counts.

## Dokumentation
[Dokumentation](https://jona-sh.github.io/V93_BP_Simulation_von_Quantenschaltungen/index.html)

## Features

- Simulation through the Qiskit Aer backend.
- A NumPy tensor-based backend using `numpy.einsum`.
- An explicit Python-loop backend.
- A Numba-compiled loop backend.
- Support for single-qubit gates and controlled-NOT gates in the einsum
  implementation.
- Reusable configuration and result objects.
- Sphinx API documentation generated from Python docstrings.

## Requirements

- Python 3.13 or newer.
- [uv](https://docs.astral.sh/uv/) is recommended for managing the project
  environment.

## Installation

From the repository root, install the project and its dependencies with:

```console
uv sync
```

## Usage

```python
from qiskit import QuantumCircuit

import q_simulator as qs

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)

config = qs.Configuration(
    method="einsum",
    number_of_shots=1024,
)
result = qs.simulate(circuit, config)

print(result.statevector)
print(result.counts)
```

The available simulation methods are:

- `"default"`: uses Qiskit Aer.
- `"einsum"`: applies gates using NumPy tensor operations.
- `"loop"`: applies gates using explicit Python loops.
- `"numba"`: applies gates using Numba-compiled loops.

If no configuration is supplied explicitly, `Configuration` defaults to the
`"default"` method and `2**16` shots.

## Testing

Run the test suite with:

```console
uv run pytest
```

## Documentation

Build the HTML documentation with:

```console
uv run .\make.bat html
```

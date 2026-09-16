# q_simulator

`q_simulator` is an educational quantum-circuit simulator developed for the
University of Stuttgart practical course *Simulation von Quantenschaltungen*.
It accepts Qiskit `QuantumCircuit` objects and returns the resulting
statevector together with measurement probabilities or counts.

## Features

- Simulation through the Qiskit Aer backend.
- A NumPy tensor-based backend using `numpy.einsum`.
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
uv run sphinx-build -b html docs docs/_build/html
```

The generated documentation is written to `docs/_build/html`.

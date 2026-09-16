Installation
============

The project requires Python 3.13 or newer. Install it with
`uv <https://docs.astral.sh/uv/>`_ from the repository root:

.. code-block:: console

   uv sync

Run the test suite with:

.. code-block:: console

   uv run pytest

Build the HTML documentation with:

.. code-block:: console

   uv run sphinx-build -b html docs docs/_build/html

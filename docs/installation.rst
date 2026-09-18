Installation
============

The project requires Python 3.13 or newer. Install it with

.. code-block:: console

   uv add install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ q_simulator_bp_feljon




.. code-block:: console

   python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ q_simulator_bp_feljon


---------

or with `uv <https://docs.astral.sh/uv/>`_ from the repository root:

.. code-block:: console

   uv sync

---------

Run the test suite with:

.. code-block:: console

   uv run pytest

Build the HTML documentation with running the following command in the docs folder:

.. code-block:: console

   uv run .\make.bat html

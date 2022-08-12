.. image:: _static/logo.png
   :alt: CIJOE

==================================================
 cijoe: tools for systems development and testing
==================================================

**cijoe** is a means to collect, and loosely formalize, the bits and pieces
commonly used during systems development in order to obtain an **automated**
and **reproducible** workflow. **cijoe** comes in handy regardless of whether
your development environment consist of a single machine, a collection of
locally available hardware resources, virtual machines, integrated **CI/CD**
pipelines, or a mixture thereof.

.. code-block:: bash

  # Install CIJOE
  python3 -m pip install --user cijoe

  # Create a default configuration and workflow
  joe -s

  # Run the example workflow, locally
  joe

The :ref:`sec-quickstart` section is provided for the impatient reader. For a
thorough description, the rest of the documentation is provided with the
:ref:`sec-introduction` serving as the starting point.

Contents:

.. toctree::
   :maxdepth: 2
   :includehidden:

   quickstart.rst
   introduction/index.rst
   prerequisites/index.rst
   installation/index.rst

   configs/index.rst
   workflows/index.rst
   worklets/index.rst

   packages/index.rst

   ssh/index.rst

   api/index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

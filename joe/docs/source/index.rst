.. image:: _static/logo.png
   :alt: CIJOE

==================================================
 cijoe: tools for systems development and testing
==================================================

**cijoe** is a means to collect, and loosely formalize, the bits and pieces
commonly used during systems development in order to obtain an **automated**
and **reproducible** workflow.

Quickstart
==========

First, install **cijoe**:

.. literalinclude:: 000_install.cmd
   :language: bash

Then, produce an default configuration file and a workflow example:

.. literalinclude:: 100_example.cmd
   :language: bash

Have, a look in your current workdir directory, the following files should be
there:

.. literalinclude:: 150_example.out
   :language: bash

Then go ahead and run it:

.. literalinclude:: 200_run.cmd
   :language: bash

.. literalinclude:: 200_run.out
   :language: bash

For a thorough description, the rest of the documentation is provided with the
:ref:`sec-introduction` serving as the starting point.

Contents:

.. toctree::
   :maxdepth: 2
   :includehidden:

   introduction/index.rst
   prerequisites/index.rst
   installation/index.rst

   configs/index.rst
   workflows/index.rst
   worklets/index.rst
   resources/index.rst

   packages/index.rst

   ssh/index.rst

   api/index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

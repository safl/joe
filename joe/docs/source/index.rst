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

The following will install **cijoe**, produce a default configuration, and an
example workflow, and execute the workflow using the configuration, and lastly
produce a workflow-report:

.. literalinclude:: 200_quickstart.cmd
   :language: bash

**cijoe** is by default silent, as in, does not print out anything unless
errors occur. Thus, to get an overview of what happened above, then produce a
report by invoking:

.. literalinclude:: 250_quickstart.txt
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
   resources/index.rst

   testing/index.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

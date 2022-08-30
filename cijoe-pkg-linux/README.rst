===========================================================================
 cijoe-pkg-linux: worklets and modules for Linux tools and kernel features
===========================================================================

.. image:: https://img.shields.io/pypi/v/cijoe-pkg-linux.svg
   :target: https://pypi.org/project/cijoe-pkg-linux
   :alt: PyPI

.. image:: https://github.com/refenv/cijoe-pkg-linux/workflows/selftest/badge.svg
   :target: https://github.com/refenv/cijoe-pkg-linux/actions
   :alt: Build Status

Install
=======

The package is distributed via PyPi, run the following to command to install:

.. code-block:: bash

  python3 -m pip install --user cijoe-pkg-linux

To install the development preview, install:

.. code-block:: bash

  python3 -m pip install --user --pre cijoe-pkg-linux

See the `Cijoe` for additional documentation.

If you find bugs or need help then feel free to submit an `Issue`_. If you want
to get involved head over to the `GitHub page`_ to get the source code and
submit a `Pull request`_ with your changes.

Test-target Environment
=======================

On your dev-box, ensure you have qemu armed and ready, and your
target-environment file providing locations, see the configuration examples for
reference.

.. _Cijoe: https://cijoe.readthedocs.io/

.. _GitHub page: https://github.com/refenv/cijoe-pkg-linux
.. _Pull request: https://github.com/refenv/cijoe-pkg-linux/pulls
.. _Issue: https://github.com/refenv/cijoe-pkg-linux/issues

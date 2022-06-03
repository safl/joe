=====
 JOE
=====

Prototype of CIJOE implemented using:

* environment definition using yaml instead of bash with variable-definitions

* The core-module of CIJOE is re-implemented as a Python class with methods:
  - cmd, push, pull

* pytest instead of ``cij_runner``; testcases, testsuites, and testplans
  replaced by pytest tests
  - thus removal of "testsuites" and "testplans"
  - re-implementation of testcases as Python using the cijoe helper for
    retargeting tests and data-transfer

* The Bash modules for ssh, qemu, fio, xnvme, spdk, etc. are re-implemented in
  Python

CIJOE provides a convenient means to automate the bunch of shell-commands used
during systems development and testing. This is lost as Bash is gone, it can
partly be regained by using the Python Shell ``xonsh``. However, still need
quite a bit of exploring before a proper replacement is found.

Todo
----

* How can this be used for scripting? E.g. the current use of CIJOE for
  deploying qemu on github, along with invoking tests. instrumenting qemu etc.

* Experiment with using fixtures for the different CIJOE hooks

* Experiment with fixture parameterization for e.g. xNVMe backend
  instrumentation

* Adjust remaining CIJOE tools to operate without the ``trun.yml``
  The most interesting tools are:
  - ``cij_reporter``
  - ``cij_extractor``

* Try setting up an auxilary package
  - It should be possible to extend with new extractors, same as
    ``cijoe-pkg-fio`` does now.
  - Possible to provide pytest-fixtures for re-use by others? E.g. have
    ``cijoe-pkg-fio`` provide the fio-execution encapsulation, the
    metric-extract. Same for ``cijoe-pkg-xnvme``, enable it to provide the
    driver-hooks etc. via fixtures.

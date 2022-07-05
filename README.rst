=====
 JOE
=====

The current CIJOE implementation is 3500 lines of Python (2500) and Shell
(900), can we do this in less than 1000 SLOC? That is, make is encredibly
simple, such that debugging it, getting to use it etc. is super simple, and in
case things are weird the source should be easy to comprehend.

Prototype of CIJOE implemented using:

* Environment definition using Yaml instead of Bash with variable-definitions

* The core-module of CIJOE is re-implemented as a Python class with methods:
  - cmd, push, pull
  - Perhaps this should be refactored to: "get()/put() and execute()"?
    - run() / get() / put()
    - execute() / download() / upload()

* pytest instead of ``cij_runner``; testcases, testsuites, and testplans
  replaced by pytest tests
  - thus removal of "testsuites" and "testplans"
  - re-implementation of testcases as Python using the cijoe helper for
    retargeting tests and data-transfer

* We might still need testplans... they will probably just be more of a
  "planning" type of thing, e.g. tell CIJOE where to collect tests from, which
  collection filters to apply, environment variables to setup and stuff like
  that. E.g. a static specification of invoking pytest, with the additional
  power of providing envionment variable definitions to the ``cijoe.run``
  instance.

* The Bash modules for ssh, qemu, fio, xnvme, spdk, etc. are re-implemented in
  Python

CIJOE provides a convenient means to automate the bunch of shell-commands used
during systems development and testing. This is lost as Bash is gone, it can
partly be regained by using the Python Shell ``xonsh``. However, still need
quite a bit of exploring before a proper replacement is found.

Since, everything needs redoing, then might as well clean up the command-line
interface and provide a single command using Python entry-points and
package-__main__. The former provides a neat ``cijoe`` executable, the latter,
in case of ``$PATH`` issues can be ignored since it is invokable via ``python3
-m cijoe.cli``.

Revamping the CLI
=================

The CIJOE command-line interface has a bunch of ``cij_*`` commands::

  cij_analyser, cij_fetch, cij_plotter, cij_root, cij_selftest, cij_tlint,
  cij_extractor, cij_metric_dumper, cij_reporter, cij_runner, cij_testcases,
  cij_trun_to_junit

be neat to re-organize these into **super** CLI with an interface along the
lines of::

  usage: joe [-h] [--version] {pytest,extract,analyse,report} ...

  positional arguments:
    {pytest,extract,analyse,report}
                          sub-command help
      pytest              bar
      extract             bar
      analyse             foo
      report              baz

  optional arguments:
    -h, --help            show this help message and exit
    --version             Show version

This has a couple of advantages:

* It will no longer require the user modying their ``$PATH`` to include the
  location of where these tools are, since this can be handled as a package
  entry-point to the **super** CLI, and invoked with: ``python3 -m cijoe.cli``

Additionally, some of these can be replaced by using Python package-features.
Also, since all the Bash-ishms, will be gone, then the ``cij_root`` is no
longer needed. Neither are ``cij_testcases`` as this is handled by ``pytest``.
Also, ``cij_selftest`` can be replaced by::

  pytest --pyargs cijoe.selftest

To avoid the addition of 

Intended Runner Invocation
==========================



Todo
====

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

Refactoring
===========

Prototype of a CIJOE refactor focusing on:

* Remove Bash from CIJOE
  - Requires re-implementing at least: core, qemu, fio

* Replace the test-runner 'cij_runner' with 'pytest'
  - This will most likely not be done in a compatible fashion with the trun-data-struct
  - Requires re-doing auxilary output generation and handling
  - Requires re-implementing extractors, analyzers, plotters etc.

Observations
------------

test_target environment variables; forwarding of environment variables, either
defined in the env.yaml or passed directly in a testcase can be passed with
less friction than in the Bash-based approach. Atleast for the Popen part, lets
see how paramiko handles it.

By using paramiko, a SSH session can be kept alive instead of re-establishing
connection for the command. This is a change in behavior which may or may not
be great. I wonder whether mosh could be used as a transport here as well.

It would seem like, with paramiko we can better separate whether the executed
command failed or the SSH layer. This is a very nice improvement.

The current Transport using command-execution via paramiko is something I am
certain will dead-lock, it needs a lot of love. Should read the buffers and
write them to logfile until the command ends. The returncode is missing as
well.

Related Work
============

CIJOE in this form seems related to the Fabric project. Atleast both projects
use Paramiko to invoke commands over SSH in a retargettable fashion. It might
be worth investigating whether the ``joe/core/transport.py`` should/could be
replaced by Fabric.

Self-testing
============

Introducing the following selftest convention:

* ``python3 -m pip pytest --pyargs joe.<pkg>.selftest``

CIJOE and packages should provide such as PyTest to "check itself". E.g. a
package providing a bunch of system-wrappers should have some basic
verification of those wrappers, it is should be easy to verify that they work.

Environment Definition
======================

CIJOE should support multiple environment definitions, that is, to combine
them. E.g. one could define the transport, another NVMe devices etc.

API Docs
========

By going all-in on Python, then CIJOE could provide API docs for everything,
core and packages. That would be neat.

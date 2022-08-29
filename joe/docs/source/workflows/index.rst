.. _sec-workflow:

Workflow
========

Not unlike the use of Yaml in Ansible and GitHUB Actions.

Workflow Files
--------------

Workflow files are formated using `YAML`_ and named with suffix
``.workflow``.

Example
-------

.. literalinclude:: example.workflow
   :language: yaml
   :caption:

Linting
-------

.. literalinclude:: 200_lint.cmd
   :language: bash

.. literalinclude:: 200_lint.out
   :language: bash


.. _YAML: https://yaml.org/

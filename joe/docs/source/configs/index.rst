.. _sec-configuration:

Configuration
=============

.. _sec-configuration-files:

Configuration Files
-------------------

Configuration files are formated using `YAML`_ and named with suffix
``.config``. In the core functionality of provided by cijoe, only the key
``transport`` has special meaning.

Keys are otherwise granted meaning by their use of :ref:`sec-worklets`,
:ref:`sec-testing`, and regular Python modules.

.. _sec-configuration-files-example:

Example
~~~~~~~

...

.. _sec-configuration-objects:

Configuration Objects
---------------------

Represented in the code as a :ref:`sec-resources`.

.. autoclass:: joe.core.resources.Config
   :members:
   :undoc-members:
   :inherited-members:

.. _YAML: https://yaml.org/

"""
    This is an attempt at making providing a super-expandable system, these worklets
    auto-populate the cli-tool, can be used in the workflow steps, and lets see what
    else they can be used for...

    Previously for the extractor a "plugin" system was used, also, everything where
    collections of bash-scripts relying on a naming-conventions. This "worklet" approach
    goes beyond that, producing a general project-infra where everything is extendable
    and auto-populated, so even the core infra of extract, metrics etc. are implemented
    using the same worklet interface, thus the interface is rigourously exercised

    The implementation relies heavily on built-in Python introspection features as well
    as 'setuptools', it is thus excessively complecated logic, relying on the intricate
    behavior of:

    * importlib.import_module()
    * setuptools.find_namespace_packages()
    * pkgutil.iter_modules()

    Currently only collecting worklets from namespace packages, however, this should
    probably be extended to do collection from local non-installed modules. All of this
    auto-collection might also quickly become very slow...
"""
import importlib
import inspect
import os
import pkgutil

import setuptools

WORKLET_FUNCTION_NAME = "worklet_entry"


def iter_packages(namespace):
    """Yield Python packages by the given 'namespace'"""

    namespace_package = importlib.import_module(namespace)
    for namespace_package_path in list(set(namespace_package.__path__)):
        for package_name in setuptools.find_namespace_packages(
            where=namespace_package_path, include=f"{namespace}.*"
        ):
            package_name = f"{namespace}.{package_name}"
            package = importlib.import_module(package_name, package=namespace)

            module_names = []
            if package.__file__ is not None:
                package_path = os.path.dirname(package.__file__)
                module_names = [
                    name for _, name, _ in pkgutil.iter_modules([package_path])
                ]

            yield package_name, module_names, package


def load_worklets_from_packages(namespace=None):
    """Load worklets namespace packages installed on the system"""

    if namespace is None:
        namespace = "joe"

    worklets = {}
    for package_name, module_names, _ in iter_packages(namespace):
        for module_name in module_names:
            mod = importlib.import_module(f"{package_name}.{module_name}", package_name)
            for function_name, function in inspect.getmembers(mod, inspect.isfunction):
                if function_name == WORKLET_FUNCTION_NAME:
                    worklets[module_name] = function

    return worklets

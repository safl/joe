import importlib
import os
import pkgutil

import setuptools

ENCODING = "UTF-8"


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


def load_scriptlet(package_name, module):
    """Load scriptlet function from the given 'package_name.module'"""

    mod = importlib.import_module(f"{package_name}.{module}", package_name)
    for function_name, function in inspect.getmembers(mod, inspect.isfunction):
        if function_name == "run":
            return function

    return None

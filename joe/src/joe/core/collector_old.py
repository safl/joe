"""
    This is an attempt at making providing a super-expandable system, these worklets
    auto-populate the cli-tool, can be used in the workflow steps, and lets see what
    else they can be used for, I guess anywhere as they can be provided anywhere, easily

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

"""
import ast
import importlib
import inspect
import os
import pkgutil
import pprint
from importlib.machinery import SourceFileLoader
from pathlib import Path

import setuptools

import joe.core.configs
import joe.core.templates
import joe.core.testfiles

WORKLET_PACKAGE_NAME = "worklets"
WORKLET_FUNCTION_NAME = "worklet_entry"

RESOURCES = {
    "templates": "html",
    "testfiles": "preqs",
    "configs": "config",
}


def collect_resources():
    """Returns a dictionalty of paths to built-in resources"""

    resources = {}
    for key, val in RESOURCES.items():
        resources[key] = [
            str(fpath)
            for fpath in importlib.resources.files(f"joe.core.{key}").rglob(f"*.{val}")
        ]

    return resources


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
    """Load worklets from installed packages"""

    if namespace is None:
        namespace = "joe"

    worklets = {}
    for package_name, mod_names, _ in iter_packages(namespace):
        if not package_name.endswith(WORKLET_PACKAGE_NAME):
            continue

        for mod_name in mod_names:
            comp = package_name.split(".")
            assert len(comp) >= 3, "Invalid assumption of worklet package name"

            # construct worklet-ident as: joe.core.worklets.something -> core.something
            ident = ".".join(comp[1:-1] + [mod_name])

            mod = importlib.import_module(f"{package_name}.{mod_name}", package_name)
            for function_name, function in inspect.getmembers(mod, inspect.isfunction):
                if function_name == WORKLET_FUNCTION_NAME:
                    worklets[ident] = function
                    break

    return worklets


def iter_modules_in_path(path=None, max_depth=2):
    """Yields absolute paths to Python modules, topdown starting at the given 'path'"""

    if path is None:
        path = Path.cwd().resolve()

    base = len(str(path).split(os.sep))
    for search in Path(path).resolve().rglob(f"*.py"):
        level = len(str(search).split(os.sep))
        if max_depth and level > base + max_depth:
            continue

        yield search


def load_worklets_from_path(path=None, depth=2):
    """Loads worklets from modules found in the given path"""

    worklets = {}

    for search_path in iter_modules_in_path(path, depth):
        with open(search_path, "r") as source:
            tree = ast.parse(source.read())

        for node in [x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]:
            if node.name != WORKLET_FUNCTION_NAME:
                continue

            mod = SourceFileLoader("", str(search_path)).load_module()
            for function_name, function in inspect.getmembers(mod, inspect.isfunction):
                if function_name == WORKLET_FUNCTION_NAME:
                    mod_name = Path(search_path).stem
                    worklets[mod_name] = function
                    break

    return worklets

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

    Currently only collecting worklets from namespace packages, however, this should
    probably be extended to do collection from local non-installed modules. All of this
    auto-collection might also quickly become very slow... to avoid searching all
    modules then worklet-modules must be named "worklet_"
"""
import importlib
import inspect
import os
import pkgutil
from pathlib import Path

import setuptools

import joe.core.configs
import joe.core.templates
import joe.core.testfiles

WORKLET_PACKAGE_NAME = "worklets"
WORKLET_FUNCTION_NAME = "worklet_entry"


def iter_config_fpaths():
    """Iterate builtin template file-paths"""

    for fpath in importlib.resources.files(joe.core.configs).rglob("*.config"):
        yield fpath


def iter_template_fpaths():
    """Iterate builtin template file-paths"""

    for fpath in importlib.resources.files(joe.core.templates).rglob("*.html"):
        yield fpath


def iter_testfile_fpaths():
    """Iterate builtin template file-paths"""

    for fpath in importlib.resources.files(joe.core.testfiles).rglob("*.preqs"):
        yield fpath


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

            mod = importlib.import_module(f"{package_name}.{mod_name}", package_name)
            for function_name, function in inspect.getmembers(mod, inspect.isfunction):
                if function_name == WORKLET_FUNCTION_NAME:
                    worklets[mod_name] = function
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
    """Loads workloads from modules found in the given path"""

    worklets = {}

    search_paths = set([str(p.parent) for p in iter_modules_in_path(path, depth)])

    for loader, mod_name, is_pkg in pkgutil.iter_modules(list(search_paths)):
        if is_pkg:
            continue

        mod = loader.find_module(mod_name).load_module(mod_name)
        for function_name, function in inspect.getmembers(mod, inspect.isfunction):
            if function_name == WORKLET_FUNCTION_NAME:
                worklets[mod_name] = function
                break

    return worklets

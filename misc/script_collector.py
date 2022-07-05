#!/usr/bin/env python3
import importlib
import pkgutil
import inspect
import os

from joe.core.collector import iter_packages, load_worklets_from_packages

WORKLET_MODULE_PREFIX = "worklet_"
WORKLET_FUNCTION_NAME = "worklet_entry"

def iter_modules_in_path(path=None, max_depth=2):
    """Yields absolute paths to Python modules, topdown starting at the given 'path'"""

    if path is None:
        path = "."

    path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))

    base = len(path.split(os.sep))
    for root, dirs, files in os.walk(path, topdown=True):
        level = len(root.split(os.sep))
        if max_depth and level > base + max_depth:
            break

        for filename in files:
            if not (filename.startswith(WORKLET_MODULE_PREFIX)):
                break
            yield os.path.join(root, filename)


def load_worklets_from_path(path=None, depth=2):

    worklets = {}

    search_paths = set([os.path.dirname(p) for p in iter_modules_in_path(path, depth)])

    for loader, mod_name, is_pkg in pkgutil.iter_modules(list(search_paths)):
        comp = mod_name.split(WORKLET_MODULE_PREFIX)
        if len(comp) != 2 or is_pkg:
            continue

        worklet_name = comp[1]
        mod = loader.find_module(mod_name).load_module(mod_name)

        for function_name, function in inspect.getmembers(mod, inspect.isfunction):
            if function_name == WORKLET_FUNCTION_NAME:
                worklets[worklet_name] = function
                break

    return worklets

def main():

    worklets = {}

    worklets = load_worklets_from_path(".", depth=2)
    print(worklets)

if __name__ == "__main__":
    main()

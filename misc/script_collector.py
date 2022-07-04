#!/usr/bin/env python3
import importlib
import inspect

from joe.core.misc import iter_packages

def main():

    for package_name, module_names, package in iter_packages("joe"):
        if "wrapper" not in module_names:
            continue

        mod = importlib.import_module(f"{package_name}.wrapper", package_name)
        for jazz in inspect.getmembers(mod, inspect.isfunction):
            print(jazz)

if __name__ == "__main__":
    main()

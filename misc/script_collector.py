#!/usr/bin/env python3
import importlib
import inspect

from joe.core.misc import iter_packages, load_scriptlet


def main():

    for package_name, module_names, package in iter_packages("joe"):
        if "wrapper" not in module_names:
            continue

        scriptlet = load_scriptlet(package_name, "wrapper")
        help(scriptlet)


if __name__ == "__main__":
    main()

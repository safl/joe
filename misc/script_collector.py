#!/usr/bin/env python3
import importlib
import inspect

from joe.core.collector import iter_packages, load_worklets_from_packages


def main():

    worklets = load_worklets_from_packages()
    for name, func in worklets.items():
        print(func.__doc__)


if __name__ == "__main__":
    main()

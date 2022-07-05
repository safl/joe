#!/usr/bin/env python3
import importlib
import pkgutil
import inspect
import os

from joe.core.collector import load_worklets_from_packages, load_worklets_from_path


def main():

    worklets = {}

    worklets = load_worklets_from_path(".", depth=2)
    print(worklets)

if __name__ == "__main__":
    main()

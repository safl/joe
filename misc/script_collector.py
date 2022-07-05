#!/usr/bin/env python3
import importlib
import inspect

from joe.core.collector import iter_packages, load_worklets_from_packages


def main():

    worklets = load_worklets_from_packages()
    print(worklets)


if __name__ == "__main__":
    main()

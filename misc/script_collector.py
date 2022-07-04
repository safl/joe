#!/usr/bin/env python3
import importlib
import inspect

from joe.core.misc import iter_packages, load_scriptlets


def main():

    scriptlets = load_scriptlets()
    print(scriptlets)


if __name__ == "__main__":
    main()

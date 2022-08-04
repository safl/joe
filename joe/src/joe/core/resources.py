#!/usr/bin/env python3
import ast
import importlib
import inspect
import os
import pkgutil
import pprint
from importlib.machinery import SourceFileLoader
from pathlib import Path

import joe
import setuptools


class Resource(object):
    """CIJOE resource"""

    def __init__(self, path: Path, pkg=None):

        self.path = path.resolve()
        self.pkg = pkg

        self.path = path
        self.content = None

        prefix = ".".join(pkg.name.split(".")[1:-1]) + "." if pkg else ""

        self.ident = f"{prefix}{self.path.stem}"

    def __repr__(self):

        return f"{self.ident}({str(self.path)})"

    def content_from_file(self):
        """Load resource-content from 'self.path'"""

        with open(self.path, "r") as resource:
            self.content = resource.read()


class Worklet(Resource):
    """A CIJOE worklet"""

    NAMING_CONVENTION = "worklet_entry"

    def __init__(self, path, pkg=None):
        super().__init__(path, pkg)

        self.func = None
        self.mod = None
        self.mod_name = None
        self.id = None

    def content_has_worklet_func(self):
        """Checks whether the resource-content has the worklet entry-function"""

        tree = ast.parse(self.content)
        for node in [x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]:
            if node.name != Worklet.NAMING_CONVENTION:
                continue

            return True

        return False

    def load(self):
        """Loads the module and the worklet-entry function"""

        if self.func:
            return True

        if not self.content:
            self.content_from_file()

        if not self.content_has_worklet_func():
            return False

        mod = SourceFileLoader("", str(self.path)).load_module()
        for function_name, function in inspect.getmembers(mod, inspect.isfunction):
            if function_name != Worklet.NAMING_CONVENTION:
                continue

            self.mod = mod
            self.mod_name = Path(self.path).stem
            self.func = function
            return True

        return False


class Collection(object):
    """Collects resources from installed packages and the current working directory"""

    RESOURCES = ["worklets", "configs", "templates", "testfiles"]
    IGNORE = ["__init__.py", "__pycache__"]

    def __init__(self):
        self.resources = {r: {} for r in Collection.RESOURCES}

    def collect_worklets_from_path(self, path=None, max_depth=2):
        """Collects non-packaged worklets from the given 'path'"""

        if path is None:
            path = Path.cwd().resolve()

        base = len(str(path).split(os.sep))

        for candidate in Path(path).resolve().rglob(f"*.py"):
            level = len(str(candidate).split(os.sep))
            if max_depth and level > base + max_depth:
                continue

            worklet = Worklet(candidate)
            worklet.content_from_file()
            if worklet.content_has_worklet_func():
                self.resources["worklets"][worklet.ident] = worklet

    def collect_from_packages(self, path=None, prefix=None):
        """Collect resources from CIJOE packages at the given path"""

        if prefix is None:
            prefix = ""

        for pkg in pkgutil.walk_packages(path, prefix):
            comp = pkg.name.split(".")[1:]  # drop the 'joe.' prefix
            if not (
                pkg.ispkg
                and any(resource in comp for resource in Collection.RESOURCES)
                and len(comp) == 2
            ):  # skip non-resource packages
                continue

            namespace, resource = comp
            for path in importlib.resources.files(f"{pkg.name}").iterdir():
                if path.name in Collection.IGNORE:
                    continue

                if resource == "worklets":
                    res = Worklet(path, pkg)
                    res.load()
                else:
                    res = Resource(path, pkg)

                self.resources[resource][res.ident] = res

    def collect(self):
        """Collect from all implemented resource "sources" """

        self.collect_from_packages(joe.__path__, "joe.")
        self.collect_worklets_from_path()

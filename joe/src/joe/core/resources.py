#!/usr/bin/env python3
"""
    CIJOE Resources

    Besides the core library, then everything else is implemented as a dynamically
    collectable and loadable resources. Whether those are worklets, auxilary testfiles,
    configuration-files, workflow-definitions etc.
    Resources are "collectable" from Python namespace-packages, as well as directly for
    the current work directory. When loading directly, then certain files are assumed to
    be of a certain type depending of their file-type:

    * .config -- CIJOE environment configurations
    * .preqs -- CIJOE performance requirements
    * .py -- CIJOE worklets
    * .workflow -- CIJOE workflow
"""
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


class Collector(object):
    """Collects resources from installed packages and the current working directory"""

    RESOURCES = {
        "configs": [".config"],
        "perf_reqs": [".perfreq"],
        "templates": [".html"],
        "testfiles": [".*"],
        "workflows": [".workflow"],
        "worklets": [".py"],
    }
    IGNORE = ["__init__.py", "__pycache__", "setup.py"]

    def __init__(self):
        self.resources = {r: {} for r in Collector.RESOURCES}

    def process_candidate(self, candidate: Path, category: str, pkg):
        """Inserts the given candidate"""

        if category == "worklets":
            resource = Worklet(candidate, pkg)
            resource.load()

            resource = Worklet(candidate, pkg)
            resource.content_from_file()

            if not resource.content_has_worklet_func():
                category = "testfiles"
        else:
            resource = Resource(candidate, pkg)

        self.resources[category][resource.ident] = resource


    def collect_from_path(self, path=None, max_depth=2):
        """Collects non-packaged worklets from the given 'path'"""

        if path is None:
            path = Path.cwd().resolve()

        base = len(str(path).split(os.sep))
        for candidate in Path(path).resolve().rglob(f"*"):
            level = len(str(candidate).split(os.sep))
            if max_depth and level > base + max_depth:
                continue

            for category, suffixes in Collector.RESOURCES.items():
                if candidate.name in Collector.IGNORE:
                    continue
                if not candidate.suffix in suffixes:
                    continue

                self.process_candidate(candidate, category, None)

    def collect_from_packages(self, path=None, prefix=None):
        """Collect resources from CIJOE packages at the given 'path'"""

        if prefix is None:
            prefix = ""

        for pkg in pkgutil.walk_packages(path, prefix):
            comp = pkg.name.split(".")[1:]  # drop the 'joe.' prefix
            if not (
                pkg.ispkg
                and any(resource in comp for resource in Collector.RESOURCES.keys())
                and len(comp) == 2
            ):  # skip non-resource packages
                continue

            _, category = comp
            for candidate in importlib.resources.files(f"{pkg.name}").iterdir():
                if candidate.name in Collector.IGNORE:
                    continue

                self.process_candidate(candidate, category, pkg)

    def collect(self):
        """Collect from all implemented resource "sources" """

        self.collect_from_packages(joe.__path__, "joe.")
        self.collect_from_path()

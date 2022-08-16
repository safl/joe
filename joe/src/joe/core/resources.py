#!/usr/bin/env python3
"""
    CIJOE Resources

    Except for the core library, then everything else is implemented as a dynamically
    collectable and loadable resources. That is, configuration-files, worklets,
    workflows, and auxilary files.

    The collection-logic is encapsulated in the joe.core.resources.Collector class
"""
import ast
import importlib
import inspect
import os
import pkgutil
from importlib.machinery import SourceFileLoader
from pathlib import Path

import setuptools

import joe


class Resource(object):
    """Base representation of a Resource"""

    def __init__(self, path: Path, pkg=None):

        self.path = path.resolve()
        self.pkg = pkg

        self.path = path
        self.content = None

        prefix = ".".join(pkg.name.split(".")[1:-1]) + "." if pkg else ""

        self.ident = f"{prefix}{self.path.stem}"

    def __repr__(self):

        return str(self.path)

    def content_from_file(self):
        """Load resource-content from 'self.path'"""

        with self.path.open("r") as resource_file:
            self.content = resource_file.read()


class Worklet(Resource):
    """Worklet representation and encapsulation"""

    NAMING_CONVENTION = "worklet_entry"

    def __init__(self, path, pkg=None):
        super().__init__(path, pkg)

        self.func = None
        self.mod = None
        self.mod_name = None

    def content_has_worklet_func(self):
        """Checks whether the resource-content has the worklet entry-function"""

        try:
            tree = ast.parse(self.content)
        except SyntaxError:
            return False

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

    RESOURCES = [
        ("configs", [".config"]),
        ("perf_reqs", [".perfreq"]),
        ("templates", [".html"]),
        ("workflows", [".workflow"]),
        ("worklets", [".py"]),
        ("auxilary", [".*"]),
    ]
    IGNORE = ["__init__.py", "__pycache__", "setup.py"]

    def __init__(self):
        self.resources = {category: {} for category, _ in Collector.RESOURCES}

    @staticmethod
    def dict_from_yamlfile(path : Path):
        """Load the yaml-file, return {} on empty document."""

        with path.open() as yamlfile:
            return yaml.safe_load(yaml_file) or {}

    @staticmethod
    def dict_substitute(topic : dict, config={}, resources={}):
        """Traverse the given 'topic', replacing {{ foo.bar }} entities with context-values"""

        errors = []

        context = {
            "local": {
                "env": os.environ,
            },
            "config": {},
            "resources": {},
        }

        jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        for key, value in topic.items():
            try:
                if isinstance(value, str):
                    topic[key] = jinja_env.from_string(value).render(context)
                elif isinstance(value, list) and all(isinstance(line, str) for line in value):
                    topic[key] = [jinja_env.from_string(line).render(context) for line in value]
                elif isinstance(value, dict):
                    errors += yaml_substitute(value)
            except jinja2.exceptions.UndefinedError as exc:
                        errors.append(f"Substitution-error: {exc}")

        return errors

    def process_candidate(self, candidate: Path, category: str, pkg):
        """Inserts the given candidate"""

        if category == "worklets":
            resource = Worklet(candidate, pkg)
            resource.content_from_file()

            if not resource.content_has_worklet_func():
                category = "auxilary"
        else:
            resource = Resource(candidate, pkg)

        self.resources[category][resource.ident] = resource

    def collect_from_path(self, path=None, max_depth=2):
        """Collects non-packaged worklets from the given 'path'"""

        path = Path(path).resolve() if path else Path.cwd().resolve()

        base = len(str(path).split(os.sep))

        for candidate in list(path.glob("*")) + list(path.glob("*/*")):
            level = len(str(candidate).split(os.sep))
            if max_depth and level > base + max_depth:
                continue

            for category, suffixes in Collector.RESOURCES:
                if candidate.name in Collector.IGNORE:
                    continue
                if candidate.suffix not in suffixes:
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
                and any(cat in comp for cat, _ in Collector.RESOURCES)
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

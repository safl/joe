import argparse
import os
from pathlib import Path

import yaml

from joe.core.collector import (
    iter_config_fpaths,
    iter_template_fpaths,
    iter_testfile_fpaths,
    load_worklets_from_packages,
    load_worklets_from_path,
)
from joe.core.command import Cijoe, config_from_file, default_output_path
from joe.core.workflow import run_workflow_files, workflow_lint


def run(args):
    """Run stuff"""

    return run_workflow_files(args)


def lint(args):
    """Lint a workflow"""

    return 0


def testfiles(args, resources):
    """List the reference configuration files provided with cijoe packages"""

    print("# Testfiles for auxilary input to testcases")
    print(yaml.dump({"testfile_fpaths": [str(r) for r in resources["testfiles"]]}))

    return 0


def templates(args, resources):
    """List the reference configuration files provided with cijoe packages"""

    print("# Template files for e.g. reporting")
    print(yaml.dump({"template_fpaths": [str(r) for r in resources["templates"]]}))

    return 0


def configs(args, resources):
    """List the reference configuration files provided with cijoe packages"""

    print("# Environment Configuration Files")
    print(yaml.dump({"config_fpaths": [str(r) for r in resources["configs"]]}))

    return 0


def worklets(args, resources):
    """List worklets provided with cijoe packages and in the cwd"""

    print(
        yaml.dump(
            {
                "worklets": {
                    name: func.__doc__ for name, func in resources["worklets"].items()
                }
            }
        )
    )

    return 0


def parse_args():
    """Parse command-line interface."""

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="func", help="sub-command help")

    parsers = {}
    parsers["run"] = subparsers.add_parser("run", help="Run workflows and worklets")
    parsers["run"].set_defaults(func=run)
    parsers["run"].add_argument(
        "--config", help="Path to the environment configuration file"
    )
    parsers["run"].add_argument(
        "--output", default=default_output_path(), help="Path to output directory"
    )
    parsers["run"].add_argument(
        "file_or_dir",
        nargs="*",
        type=Path,
        default=[Path.cwd()],
        help="Path to one of more workflow.yaml or worklet_NAME.py files",
    )

    parsers["lint"] = subparsers.add_parser(
        "lint", help="Check the integrity of the given workflow"
    )
    parsers["lint"].set_defaults(func=lint)
    parsers["lint"].add_argument(
        "workflow", help="Path to workflow file e.g. 'my.workflow'"
    )

    resources = {
        "configs": configs,
        "templates": templates,
        "testfiles": testfiles,
        "worklets": worklets,
    }
    for name, func in resources.items():
        parsers[name] = subparsers.add_parser(name, help=f"List {name}")
        parsers[name].set_defaults(func=func)

    args = parser.parse_args()

    resources = {}
    resources["configs"] = list(iter_config_fpaths())
    resources["templates"] = list(iter_template_fpaths())
    resources["testfiles"] = list(iter_testfile_fpaths())
    resources["worklets"] = load_worklets_from_packages()
    #resources["worklets"].update(load_worklets_from_path(Path.cwd()))

    return args, resources


def main():
    """Main entry point for the CLI"""

    args, resources = parse_args()
    if args.func:
        args.func(args, resources)

import argparse
import os
from pathlib import Path

import yaml

from joe.core.collector import (
    collect_resources,
    load_worklets_from_packages,
    load_worklets_from_path,
)
from joe.core.command import Cijoe, config_from_file, default_output_path
from joe.core.workflow import run_workflow_files, workflow_lint


def sub_run(args, resources):
    """Run stuff"""

    return run_workflow_files(args, resources)


def sub_lint(args, resources):
    """Lint a workflow"""

    return 0


def sub_resources(args, resources):
    """List the reference configuration files provided with cijoe packages"""

    print("# Core resources")
    try:
        print(yaml.dump(resources))
    except Exception as exc:
        print(exc)

    return 0


def sub_worklets(args, resources):
    """List worklets provided with cijoe packages and in the cwd"""

    print("# Worklets discovered in packages and current-working-dir")
    try:
        print(
            yaml.dump(
                {
                    "worklets": {
                        name: func.__doc__
                        for name, func in resources["worklets"].items()
                    }
                }
            )
        )
    except Exception as exc:
        print(exc)

    return 0


def parse_args():
    """Parse command-line interface."""

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="func", help="sub-command help")

    parsers = {}

    parsers["run"] = subparsers.add_parser("run", help="Run workflows and worklets")
    parsers["run"].set_defaults(func=sub_run)
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
    parsers["lint"].set_defaults(func=sub_lint)
    parsers["lint"].add_argument(
        "workflow", help="Path to workflow file e.g. 'my.workflow'"
    )

    parsers["resources"] = subparsers.add_parser("resources", help=f"List resources")
    parsers["resources"].set_defaults(func=sub_resources)

    parsers["worklets"] = subparsers.add_parser("worklets", help=f"List worklets")
    parsers["worklets"].set_defaults(func=sub_worklets)

    args = parser.parse_args()

    try:
        resources = collect_resources()
        resources["worklets"] = load_worklets_from_packages()
        resources["worklets"].update(load_worklets_from_path(Path.cwd()))
    except Exception as exc:
        print("Huha", exc)
        resources = {}

    return args, resources


def main():
    """Main entry point for the CLI"""

    args, resources = parse_args()
    if args.func:
        args.func(args, resources)

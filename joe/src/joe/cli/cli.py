import argparse
import os
from pathlib import Path

import yaml

from joe.core.collector import load_worklets_from_packages, load_worklets_from_path
from joe.core.command import Cijoe, config_from_file, default_output_path
from joe.core.workflow import run_workflow_files, workflow_lint


def run(args):
    """Run stuff"""

    return run_workflow_files(args)


def worklets(args):
    """List worklets provided with cijoe packages and in the cwd"""

    print(
        yaml.dump(
            {"worklets": {name: func.__doc__ for name, func in args.worklets.items()}}
        )
    )


def configs(args):
    """List the reference configuration files provided with cijoe packages"""

    print("configuration-files")

    return 0


def lint(args):
    """Lint a workflow"""

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

    parsers["configs"] = subparsers.add_parser(
        "configs", help="List reference configuration files"
    )
    parsers["configs"].set_defaults(func=configs)

    parsers["worklets"] = subparsers.add_parser(
        "worklets",
        help="List worklets provided via packages and current-working-directory",
    )
    parsers["worklets"].set_defaults(func=worklets)

    args = parser.parse_args()

    args.worklets = load_worklets_from_packages()
    args.worklets.update(load_worklets_from_path(Path.cwd()))
    # args.worklets.update(load_worklets_from_path(Path("worklets")))

    return args


def main():
    """Main entry point for the CLI"""

    args = parse_args()
    if args.func:
        args.func(args)

import argparse
import os
from pathlib import Path

import yaml

from joe.core.collector import load_worklets_from_packages, load_worklets_from_path
from joe.core.command import Cijoe, config_from_file, default_output_path
from joe.core.workflow import workflow_lint, workflow_run


def is_workflow(path):
    """Returns True when the given path is a workflow file"""

    return path.is_file and path.name.endswith(".workflow")


WORKFLOW_SUFFIX = "workflow"


def paths_to_workflow_fpaths(paths):
    """Return list of workflow files in the given list of files and directories"""

    workflow_files = []
    for path in [Path(p).resolve() for p in paths]:
        if path.is_dir():
            workflow_files.extend(
                [p for p in path.iterdir() if p.name.endswith(f"*.{WORKFLOW_SUFFIX}")]
            )
        elif path.is_file() and path.name.endswith(f".{WORKFLOW_SUFFIX}"):
            workflow_files.append(path)

    return workflow_files


def run(args):
    """Run stuff"""

    for p in paths_to_workflow_fpaths(args.file_or_dir):
        print(p)

    return 0

    # return workflow_run(args)


def list(args):
    """List different collectable resources"""

    print(
        yaml.dump(
            {"worklets": {name: func.__doc__ for name, func in args.worklets.items()}}
        )
    )


def lint(args):
    """Lint a workflow"""

    pass


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
    parsers["lint"].add_argument("workflow", help="Path to a workflow.yaml")

    parsers["list"] = subparsers.add_parser("list", help="List worklets")
    parsers["list"].set_defaults(func=list)

    # for function_name, function in worklets.items():
    #    parsers[function_name] = subparsers.add_parser(
    #        function_name, help=function.__doc__
    #    )
    #    parsers[function_name].set_defaults(func=function)
    #    parsers[function_name].add_argument(
    #        "--env", help="Path to the environment definition"
    #    )
    #    parsers[function_name].add_argument(
    #        "--output", default=default_output_path(), help="Path to test-results"
    #    )

    args = parser.parse_args()

    args.worklets = load_worklets_from_packages()
    if os.path.exists("worklets"):
        args.worklets.update(load_worklets_from_path("worklets"))

    return args


def main():
    """Main entry point for the CLI"""

    args = parse_args()
    if args.func:
        args.func(args)

import argparse
import os

from joe.core.collector import load_worklets_from_packages
from joe.core.command import Cijoe, default_output_path, env_from_file
from joe.core.workflow import workflow_lint, workflow_run

def run_workflows(args):
    """Run a list of workflows"""

    pass

def run_worklets(args):
    """Run a list of worklets"""

    pass

def run(args):
    """Run stuff"""

    pass

def list(args):
    """List different collectable resources"""

    pass

def lint(args):
    """Lint a workflow"""

    pass

def parse_args():
    """Parse command-line interface."""

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="func", help="sub-command help")

    parsers = {}
    parsers["run"] = subparsers.add_parser(
        "run", help="Run workflows and worklets"
    )
    parsers["run"].set_defaults(func=run)
    parsers["run"].add_argument(
        "--env",
        help="Path to the environment definition"
    )
    parsers["run"].add_argument(
        "--output",
        default=default_output_path(),
        help="Path to output"
    )

    group = parsers["run"].add_mutually_exclusive_group()
    group.add_argument(
        "--workflow",
        nargs='*',
        help="Path to one of more workflow files (yaml)",
    )
    group.add_argument(
        "--worklets",
        nargs='*',
        help="Name of one or more worklets to run",
    )

    parsers["lint"] = subparsers.add_parser(
        "lint", help="Check the integrity of the given workflow"
    )
    parsers["lint"].set_defaults(func=lint)
    parsers["lint"].add_argument("--workflow", help="Path to a workflow.yaml")

    worklets = load_worklets_from_packages()
    #for function_name, function in worklets.items():
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
    args.worklets = worklets

    return args


def main():
    """Main entry point for the CLI"""

    args = parse_args()
    if args.func:
        args.func(args)

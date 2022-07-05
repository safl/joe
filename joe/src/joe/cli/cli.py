import argparse

import yaml
from yaml.loader import SafeLoader

from joe.core.collector import load_worklets_from_packages


def run(args):

    with open(args.env) as env_file:
        env = yaml.load(env_file, Loader=SafeLoader)

    with open(args.workflow) as workflow_file:
        workflow = yaml.load(workflow_file, Loader=SafeLoader)

    for step in workflow.get("steps", []):
        if step not in worklets:
            return 1

        args.worklets[step](None, args)


def parse_args():
    """Parse command-line interface."""

    worklets = load_worklets_from_packages()

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="func", help="sub-command help")

    parsers = {}

    parsers["run"] = subparsers.add_parser("run", help="Process workflow")
    parsers["run"].set_defaults(func=run)
    parsers["run"].add_argument("--env", help="Path to the environment definition")
    parsers["run"].add_argument("--workflow", help="Path to a workflow.yaml")
    parsers["run"].add_argument("--output", help="Path to test-results")

    for function_name, function in worklets.items():
        parsers[function_name] = subparsers.add_parser(
            function_name, help=function.__doc__
        )
        parsers[function_name].set_defaults(func=function)
        parsers[function_name].add_argument(
            "--env", help="Path to the environment definition"
        )
        parsers[function_name].add_argument("--output", help="Path to test-results")

    args = parser.parse_args()
    args.worklets = worklets

    return args


def main():
    """Main entry point for the CLI"""

    args = parse_args()
    if args.func:
        args.func(args)

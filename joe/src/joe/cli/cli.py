import argparse
import pprint

import yaml
from yaml.loader import SafeLoader

from joe.core.collector import load_worklets_from_packages

# TODO: add a CIJOE instance
def run(args):
    """Run workflow"""

    with open(args.env) as env_file:
        env = yaml.load(env_file, Loader=SafeLoader)

    with open(args.workflow) as workflow_file:
        workflow = yaml.load(workflow_file, Loader=SafeLoader)

    anon_count = 0
    for entry in workflow.get("steps", []):
        pprint.pprint(entry)

        step = {
            "name": step["name"] = entry.get("name", None),
            "run": "",
            "with": "",
            "uses": {},
        }

        if step["name"] is None:  # Ensure that the step has a name
            anon_count += 1
            step["name"] = f"Unnamed step ({anon_count}"

        if "uses" in entry:
            step["uses"] = entry.get("uses")
            step["with"] = entry.get("with", {})

            args.worklets[worklet["id"]](None, args, step)
        elif "run" in entry:
            step["run"] = entry.get("run").strip().splitlines()
            print(step["run"])
            pass
        else:
            print("invalid step-definition")
            return 1

        # TODO: ensure a cijoe instance is available here


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

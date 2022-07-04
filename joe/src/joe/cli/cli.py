import argparse

from joe.core.misc import load_scriptlets


def run(args):
    print("invoking pytest")


def parse_args():
    """Parse command-line interface."""

    parser = argparse.ArgumentParser(prog="joe")
    parser.add_argument("--version", action="store_true", help="Show version")

    subparsers = parser.add_subparsers(dest="func", help="sub-command help")

    parsers = {}

    parsers["run"] = subparsers.add_parser("run", help="Invoke the test-runner")
    parsers["run"].set_defaults(func=run)
    parsers["run"].add_argument("--env", help="Path to the environment definition")
    parsers["run"].add_argument("--workflow", help="Path to a workflow.yaml")
    parsers["run"].add_argument("--output", help="Path to test-results")

    for function_name, function in load_scriptlets():
        parsers[function_name] = subparsers.add_parser(
            function_name, help="Invoke the scriptlet"
        )
        parsers[function_name].set_defaults(func=function)
        parsers[function_name].add_argument(
            "--env", help="Path to the environment definition"
        )
        parsers[function_name].add_argument("--output", help="Path to test-results")

    return parser.parse_args()


def main():
    """Main entry point for the CLI"""

    args = parse_args()
    if args.func:
        args.func(args)

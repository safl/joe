import argparse
import pprint
from pathlib import Path

import joe.core
from joe.core.command import default_output_path
from joe.core.resources import Collector
from joe.core.workflow import Workflow
from joe.core.misc import h1, h2, h3


def cli_lint(args, collector):
    """Lint a workflow"""

    h2("Lint")
    print(f"workflow: '{args.workflow}'")

    if args.workflow is None:
        h3("Lint: Failed(Missing workflow)")
        return 1
    h3()

    workflow = Workflow(Path(args.workflow))

    errors = workflow.lint(collector)
    for error in errors:
        print(error)

    if errors:
        h3("Lint; Failed")
        return 1

    h3("Lint; Success")

    return 0


def cli_resources(args, collector):
    """List the reference configuration files provided with cijoe packages"""

    h2("Resources")
    for category, resources in sorted(collector.resources.items()):
        print(f"{category}:" + ("" if resources.items() else " ~"))

        for ident, path in sorted(resources.items()):
            print(f"  - ident: {ident}")
            print(f"    path: {path}")

    return 0


def cli_version(args, collector):
    """Print version and exit"""

    print(f"joe {joe.core.__version__}")

    return 0


# TODO: add stats on workflow / progress
def cli_run(args, collector):
    """Run stuff"""

    h2("Run")

    if args.workflow is None:
        h3("Run: Failed(Missing workflow)")
        return 1

    print(f"workflow: {args.workflow}")
    print(f"config: {args.config}")
    h3()

    workflow = Workflow(args.workflow)
    workflow.load(collector)

    err = workflow.run(args)
    if err:
        h3("Run; Failed")
        return err

    h3("Run; Success")

    return 0


def parse_args():
    """Parse command-line interface."""

    cfiles = sorted([p.resolve() for p in Path().rglob(f"*.config")])
    wfiles = sorted([p.resolve() for p in Path().rglob(f"*{Workflow.SUFFIX}")])

    parser = argparse.ArgumentParser(prog="joe")

    parser.add_argument("step", nargs="*", help="One or more workflow steps to run.")

    parser.add_argument(
        "-w",
        "--workflow",
        default=wfiles[0] if wfiles else None,
        help="Path to Workflow file.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=cfiles[0] if cfiles else None,
        help="Path to the Configuration file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=default_output_path(),
        help="Path to output directory.",
    )

    parser.add_argument(
        "-l",
        "--lint",
        action="store_true",
        help="Check integrity of workflow and exit.",
    )
    parser.add_argument(
        "-r",
        "--resources",
        action="store_true",
        help="List collected resources and exit.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print the version number of 'joe' and exit.",
    )

    return parser.parse_args()


def main():
    """Main entry point for the CLI"""

    args = parse_args()

    collector = Collector()
    collector.collect()

    if args.lint:
        cli_lint(args, collector)
        return 0

    if args.resources:
        cli_resources(args, collector)
        return 0

    if args.version:
        cli_version(args, collector)
        return 0

    return cli_run(args, collector)

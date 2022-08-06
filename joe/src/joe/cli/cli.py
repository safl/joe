import argparse
import pprint
from pathlib import Path

from joe.core.command import default_output_path
from joe.core.resources import Collector
from joe.core.workflow import Workflow


# TODO: add stats on workflow / progress
def sub_run(args, collector):
    """Run stuff"""

    workflow_files = []
    for path in [Path(p).resolve() for p in args.file_or_dir]:
        if path.is_dir():
            workflow_files.extend(
                [p for p in path.iterdir() if p.name.endswith(f"{Workflow.SUFFIX}")]
            )
        elif path.is_file() and path.name.endswith(f"{Workflow.SUFFIX}"):
            workflow_files.append(path)

    nworkflows = len(workflow_files)

    print("#")
    print(f"# CIJOE config({args.config}), nworkflows({nworkflows})")
    print("#")

    for count, workflow_fpath in enumerate(workflow_files, 1):
        print(f"# workflow {count}/{nworkflows} -- BEGIN")

        workflow = Workflow(workflow_fpath)
        workflow.load(collector)
        err = workflow.run(args)
        if err:
            print(f"# workflow {count}/{nworkflows} -- FAILED")
            return err

        print(f"# workflow {count}/{nworkflows} -- SUCCESS")

    return 0


def sub_lint(args, collector):
    """Lint a workflow"""

    print("# Linting ...")

    workflow = Workflow(Path(args.workflow))

    errors = workflow.lint(collector)
    for error in errors:
        print(error)

    if errors:
        return 1

    return 0


def sub_resources(args, collector):
    """List the reference configuration files provided with cijoe packages"""

    print("# Resources")
    for category, resources in sorted(collector.resources.items()):
        print(f"{category}:" + ("" if resources.items() else " ~"))

        for ident, path in sorted(resources.items()):
            print(f"  - ident: {ident}")
            print(f"    path: {path}")

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

    parsers["resources"] = subparsers.add_parser("resources", help="List resources")
    parsers["resources"].set_defaults(func=sub_resources)

    args = parser.parse_args()

    collector = Collector()
    collector.collect()

    return args, collector


def main():
    """Main entry point for the CLI"""

    args, collector = parse_args()
    if args.func:
        args.func(args, collector)

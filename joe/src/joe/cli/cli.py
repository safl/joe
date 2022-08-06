import argparse
import pprint
from pathlib import Path

from joe.core.command import default_output_path
from joe.core.resources import Collector
from joe.core.workflow import Workflow


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

    for workflow_fpath in workflow_files:
        workflow = Workflow(workflow_fpath)
        workflow.load(collector)
        workflow.run(args)

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

    print("# Core resources")
    try:
        pprint.pprint(collector.resources)
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

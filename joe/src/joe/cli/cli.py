import argparse
import pprint
from pathlib import Path
import shutil

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
        h2("Lint: 'missing workflow'; Failed")
        return 1
    h3()

    workflow = Workflow(Path(args.workflow))

    errors = workflow.lint(collector)
    for error in errors:
        print(error)

    if errors:
        h2("Lint: 'see errors above'; Failed")
        return 1

    h2("Lint: 'no errors'; Success")

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


def cli_skeleton(args, collector):
    """Create skeleton .config and .workflow"""

    src_config = collector.resources["configs"]["core.default"].path
    src_workflow = collector.resources["workflows"]["core.example"].path

    dst_config = Path.cwd().joinpath(src_config.name)
    dst_workflow = Path.cwd().joinpath(src_workflow.name)

    h2("Skeleton")
    print(f"config: {dst_config}")
    print(f"workflow: {dst_workflow}")
    h3("")

    if dst_config.exists():
        print(f"skipping config({dst_config}); already exists")
    else:
        shutil.copyfile(src_config, dst_config)

    if dst_workflow.exists():
        print(f"skipping workflow({dst_workflow}); already exists")
    else:
        shutil.copyfile(src_workflow, dst_workflow)

    h2("Skeleton; Done")

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
        h2("Run: 'missing workflow'; Failed")
        return 1

    print(f"workflow: {args.workflow}")
    print(f"config: {args.config}")
    h3()

    workflow = Workflow(args.workflow)
    if not workflow.load(collector):
        h2("Run: 'workflow.load()'; Failed");
        return 1

    err = workflow.run(args)
    if err:
        h2("Run: 'workflow.run()'; Failed")
        return err

    h2("Run: 'no errors detected'; Success")

    return 0


def parse_args():
    """Parse command-line interface."""

    cfiles = sorted([p.resolve() for p in Path.cwd().iterdir() if p.suffix == ".config"])
    wfiles = sorted([p.resolve() for p in Path.cwd().iterdir() if p.suffix == ".workflow"])

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
        "-s",
        "--skeleton",
        action="store_true",
        help="Create a default '.config' and '.workflow' in `pwd` then exit.",
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
        return cli_lint(args, collector)

    if args.resources:
        return cli_resources(args, collector)

    if args.skeleton:
        return cli_skeleton(args, collector)

    if args.version:
        return cli_version(args, collector)

    return cli_run(args, collector)

import argparse
import errno
import os
import shutil
import time
from pathlib import Path

import joe.core
from joe.core.command import Cijoe, default_output_path
from joe.core.misc import h2, h3, h4
from joe.core.resources import (
    Config,
    Workflow,
    dict_from_yamlfile,
    dict_substitute,
    get_resources,
)


def print_errors(errors):
    h3("errors")
    for error in errors:
        print(errors)
    h3()


def cli_lint(args):
    """Lint a workflow"""

    h2("Lint")
    print(f"workflow: '{args.workflow}'")
    print(f"config: '{args.config}'")

    if args.workflow is None:
        h2("Lint: 'missing workflow'; Failed")
        return 1
    h3()

    workflow_dict = dict_from_yamlfile(args.workflow.resolve())
    errors = Workflow.dict_normalize(workflow_dict)  # Normalize it
    errors += Workflow.dict_lint(workflow_dict)  # Check the yaml-file

    if args.config:  # Check config/substitutions
        config = Config.from_path(args.config)
        if not config:
            h2("Lint: failed loading config")
            return 1

        errors += dict_substitute(workflow_dict, config.options)

    if errors:
        h2("Lint: 'see errors above'; Failed")
        return 1

    h2("Lint: 'no errors'; Success")

    return 0


def cli_resources(args):
    """List the reference configuration files provided with cijoe packages"""

    resources = get_resources()

    h2("Resources")
    print("Resources collected by the CIJOE collector are listed below.")
    h3()
    for category, category_resources in sorted(resources.items()):
        print(f"{category}:" + ("" if category_resources.items() else " ~"))

        for ident, path in sorted(category_resources.items()):
            print(f"  - ident: {ident}")
            print(f"    path: {path}")

    return 0


def cli_example(args):
    """Create example .config and .workflow"""

    resources = get_resources()

    resource = resources["configs"].get(f"{args.example}.default", None)
    if resource is None:
        print(f"'default.config' from '{args.example}' is not available")
        return 1
    src_config = resource.path

    resource = resources["workflows"].get(f"{args.example}.example", None)
    if resource is None:
        print(f"'example.workflow' from '{args.example}' is not available")
        return 1

    src_workflow = resource.path

    dst_config = Path.cwd().joinpath(src_config.name)
    dst_workflow = Path.cwd().joinpath(src_workflow.name)

    h2("Example")
    print(f"config: {dst_config}")
    print(f"workflow: {dst_workflow}")
    h3("")

    if not src_config.exists():
        print(f"'default.config' from '{args.example}' is not available")
        return 1
    if not src_workflow.exists():
        print(f"example.workflow' from '{args.example}' is not available")
        return 1

    if dst_config.exists():
        print(f"skipping config({dst_config}); already exists")
    else:
        shutil.copyfile(src_config, dst_config)

    if dst_workflow.exists():
        print(f"skipping workflow({dst_workflow}); already exists")
    else:
        shutil.copyfile(src_workflow, dst_workflow)

    h2("Example; Done")

    return 0


def cli_version(args):
    """Print version and exit"""

    print(f"joe {joe.core.__version__}")

    return 0


# TODO: add stats on workflow / progress
def cli_run(args):
    """Run stuff"""

    h2("Run")

    if args.workflow is None:
        h2("Run: 'missing workflow'; Failed")
        return 1
    if args.config is None:
        h2("Run: 'missing config'; Failed")
        return 1

    print(f"workflow: {args.workflow}")
    print(f"config: {args.config}")
    print(f"output: {args.output}")

    config = Config(args.config.resolve())
    errors = config.load()
    if errors:
        for error in errors:
            print(error)

        h2("Run: 'Config(args.config).load()'; Failed")
        return errno.EINVAL

    workflow = Workflow(args.workflow)
    errors = workflow.load(config)
    if errors:
        h2("Run: 'workflow.load()'; Failed")
        return 1

    step_names = [step["name"] for step in workflow.state["steps"]]
    for step_name in args.step:
        if step_name in step_names:
            continue

        h4(f"step({step_name}) not in workflow; failed")
        return errno.EINVAL

    errors = workflow.load(config)
    if errors:
        for error in errors:
            h4(error)
        h4("workflow.load(): failed; see above or by run 'joe -l'")
        return errno.EINVAL

    # TODO: copy workflow and config to directory
    os.makedirs(args.output)
    workflow.state_dump(args.output / Workflow.STATE_FILENAME)

    fail_fast = False
    resources = get_resources()

    cijoe = Cijoe(config, args.output)
    for step in workflow.state["steps"]:

        h3(f"step({step['name']})")

        begin = time.time()

        cijoe.set_output_ident(step["id"])
        os.makedirs(os.path.join(cijoe.output_path, step["id"]), exist_ok=True)

        if args.step and step["name"] not in args.step:
            step["status"]["skipped"] = 1
        else:
            worklet_ident = step["uses"]

            try:
                resources["worklets"][worklet_ident].load()
                err = resources["worklets"][worklet_ident].func(args, cijoe, step)
                if err:
                    h4(f"worklet({worklet_ident}) : err({err})")
                step["status"]["failed" if err else "passed"] = 1
            except KeyboardInterrupt as exc:
                step["status"]["failed"] = 1
                h4(f"worklet({worklet_ident}) : KeyboardInterrupt({exc})")
            except Exception as exc:
                step["status"]["failed"] = 1
                h4(f"worklet({worklet_ident}) : threw({exc})")

        for key in ["failed", "passed", "skipped"]:
            workflow.state["status"][key] += step["status"][key]

        step["status"]["elapsed"] = time.time() - begin
        workflow.state["status"]["elapsed"] += step["status"]["elapsed"]
        workflow.state_dump(args.output / Workflow.STATE_FILENAME)

        for text, status in step["status"].items():
            if text != "elapsed" and status:
                h3(f"step({step['name']}) : {text}")

        if step["status"]["failed"] and fail_fast:
            h2(f"exiting, fail_fast({fail_fast})")
            break

    rcode = errno.EIO if workflow.state["status"]["failed"] else 0

    if rcode:
        h2("Run: failed(one or more steps failed)")
    else:
        h2("Run: success")

    return rcode


def parse_args():
    """Parse command-line interface."""

    cfiles = sorted(
        [p.resolve() for p in Path.cwd().iterdir() if p.suffix == ".config"]
    )
    wfiles = sorted(
        [p.resolve() for p in Path.cwd().iterdir() if p.suffix == ".workflow"]
    )

    parser = argparse.ArgumentParser(prog="joe")

    parser.add_argument("step", nargs="*", help="One or more workflow steps to run.")

    parser.add_argument(
        "-w",
        "--workflow",
        type=Path,
        default=wfiles[0] if wfiles else None,
        help="Path to Workflow file.",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=cfiles[0] if cfiles else None,
        help="Path to the Configuration file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
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
        "-e",
        "--example",
        action="store",
        const="core",
        type=str,
        nargs="?",
        default=None,
        help="Create a 'default.config' and 'example.workflow' in `pwd` then exit.",
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

    if args.lint:
        return cli_lint(args)

    if args.resources:
        return cli_resources(args)

    if args.example:
        return cli_example(args)

    if args.version:
        return cli_version(args)

    return cli_run(args)

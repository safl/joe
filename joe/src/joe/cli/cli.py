import argparse
import errno
import logging as log
import os
import shutil
import time
from pathlib import Path

import joe.core
from joe.core.command import Cijoe, default_output_path
from joe.core.monitor import WorkflowMonitor
from joe.core.resources import (
    Config,
    Workflow,
    dict_from_yamlfile,
    dict_substitute,
    get_resources,
)


def log_errors(errors):
    for error in errors:
        log.error(error)


def cli_integrity_check(args):
    """Lint a workflow"""

    log.info("cli: lint")
    log.info(f"workflow: '{args.workflow}'")
    log.info(f"config: '{args.config}'")

    if args.workflow is None:
        log.error("'failed: missing workflow'")
        return errno.EINVAL

    workflow_dict = dict_from_yamlfile(args.workflow.resolve())
    errors = Workflow.dict_normalize(workflow_dict)  # Normalize it
    errors += Workflow.dict_lint(workflow_dict)  # Check the yaml-file

    if args.config:  # Check config/substitutions
        config = Config.from_path(args.config)
        if not config:
            log.error(f"failed: Config.from_path({args.config})")
            return errno.EINVAL

        errors += dict_substitute(workflow_dict, config.options)

    if errors:
        log_errors(errors)
        log.error("failed: 'see errors above'; Failed")
        return errno.EINVAL

    return 0


def cli_resources(args):
    """List the reference configuration files provided with cijoe packages"""

    log.info("cli: resources")
    resources = get_resources()

    print("Resources collected by the CIJOE collector are listed below.")
    for category, category_resources in sorted(resources.items()):
        print(f"{category}:" + ("" if category_resources.items() else " ~"))

        for ident, path in sorted(category_resources.items()):
            print(f"  - ident: {ident}")
            print(f"    path: {path}")

    return 0


def cli_produce_report(args):
    """Produce workflow-report"""

    if not (args.output / "workflow.state").exists():
        log.error("no workflow.state, nothing to produce a report for")
        return errno.EINVAL

    resources = get_resources()

    reporter = resources["worklets"]["core.reporter"]
    if reporter.func is None:
        reporter.load()

    return reporter.func(
        args,
        None,
        {"name": "report", "uses": "core.reporter", "with": {"report_open": True}},
    )


def cli_example(args):
    """Create example .config and .workflow"""

    log.info("cli: examples")
    rcode = 0

    resources = get_resources()

    resource = resources["configs"].get(f"{args.example}.default", None)
    if resource is None:
        log.error(f"'default.config' from '{args.example}' is not available")
        return errno.EINVAL
    src_config = resource.path

    resource = resources["workflows"].get(f"{args.example}.example", None)
    if resource is None:
        log.error(f"'example.workflow' from '{args.example}' is not available")
        return errno.EINVAL

    src_workflow = resource.path

    dst_config = Path.cwd().joinpath(src_config.name)
    dst_workflow = Path.cwd().joinpath(src_workflow.name)

    log.info(f"config: {dst_config}")
    log.info(f"workflow: {dst_workflow}")

    if not src_config.exists():
        log.error(f"'default.config' from '{args.example}' is not available")
        return errno.EINVAL
    if not src_workflow.exists():
        log.error(f"example.workflow' from '{args.example}' is not available")
        return errno.EINVAL

    if dst_config.exists():
        rcode = errno.EEXIST
        log.error(f"skipping config({dst_config}); already exists")
    else:
        shutil.copyfile(src_config, dst_config)

    if dst_workflow.exists():
        rcode = errno.EEXIST
        log.error(f"skipping workflow({dst_workflow}); already exists")
    else:
        shutil.copyfile(src_workflow, dst_workflow)

    return rcode


def cli_version(args):
    """Print version and exit"""

    print(f"joe {joe.core.__version__}")

    return 0


def cli_workflow(args):
    """Process workflow"""

    log.info("cli: run")
    log.info(f"workflow: {args.workflow}")
    log.info(f"config: {args.config}")
    log.info(f"output: {args.output}")

    if args.workflow is None:
        log.error("missing workflow")
        return errno.EINVAL
    if args.config is None:
        log.error("missing config")
        return errno.EINVAL
    state_path = args.output / "workflow.state"
    if state_path.exists():
        log.error(f"aborting; output-directory({args.output}) already exists")
        return errno.EPERM

    config = Config(args.config.resolve())
    errors = config.load()
    if errors:
        log_errors(errors)
        log.error("failed: Config(args.config).load()")
        return errno.EINVAL

    workflow = Workflow(args.workflow)

    errors = workflow.load(config)
    if errors:
        log_errors(errors)
        log.error("workflow.load(): see errors above or run 'joe -i'")
        return errno.EINVAL

    step_names = [step["name"] for step in workflow.state["steps"]]
    for step_name in args.step:
        if step_name in step_names:
            continue

        log.error(f"step({step_name}) not in workflow")
        return errno.EINVAL

    os.makedirs(args.output)
    shutil.copyfile(args.config, args.output / "config.orig")
    shutil.copyfile(args.workflow, args.output / "workflow.orig")

    workflow.state_dump(args.output / Workflow.STATE_FILENAME)

    monitor = None
    if args.monitor:
        monitor = WorkflowMonitor(str(args.output), log_level=args.log_level)
        monitor.start()

    fail_fast = False
    resources = get_resources()

    cijoe = Cijoe(config, args.output)
    for step in workflow.state["steps"]:

        log.info(f"step({step['name']}) - begin")

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
                    log.error(f"worklet({worklet_ident}) : err({err})")
                step["status"]["failed" if err else "passed"] = 1
            except KeyboardInterrupt as exc:
                step["status"]["failed"] = 1
                log.error(f"worklet({worklet_ident}) : KeyboardInterrupt({exc})")
            except Exception as exc:
                step["status"]["failed"] = 1
                log.error(f"worklet({worklet_ident}) : Raised Exception({exc})")

        for key in ["failed", "passed", "skipped"]:
            workflow.state["status"][key] += step["status"][key]

        step["status"]["elapsed"] = time.time() - begin
        workflow.state["status"]["elapsed"] += step["status"]["elapsed"]
        workflow.state_dump(args.output / Workflow.STATE_FILENAME)

        for text, status in step["status"].items():
            if text != "elapsed" and status:
                log.info(f"step({step['name']}) : {text}")

        if step["status"]["failed"] and fail_fast:
            log.error(f"exiting, fail_fast({fail_fast})")
            break

    rcode = errno.EIO if workflow.state["status"]["failed"] else 0
    if rcode:
        log.error("one or more steps failed")

    if monitor:
        monitor.stop()

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
        "--config",
        "-c",
        type=Path,
        default=cfiles[0] if cfiles else None,
        help="Path to the Configuration file.",
    )
    parser.add_argument(
        "--workflow",
        "-w",
        type=Path,
        default=wfiles[0] if wfiles else None,
        help="Path to Workflow file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=default_output_path(),
        help="Path to output directory.",
    )
    parser.add_argument(
        "--log-level",
        "-l",
        action="append_const",
        const=1,
        help="Increase log-level.",
    )
    parser.add_argument(
        "--monitor",
        "-m",
        action="store_true",
        help="Monitor workflow-output",
    )

    parser.add_argument(
        "--produce-report",
        "-p",
        action="append_const",
        const=1,
        help="Produce report for workflow in '-o / --output' and exit.",
    )
    parser.add_argument(
        "--integrity-check",
        "-i",
        action="store_true",
        help="Check integrity of workflow and exit.",
    )
    parser.add_argument(
        "--resources",
        "-r",
        action="store_true",
        help="List collected resources and exit.",
    )
    parser.add_argument(
        "--example",
        "-e",
        action="store",
        const="core",
        type=str,
        nargs="?",
        default=None,
        help="Create 'default.config' and 'example.workflow' then exit.",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Print the version number of 'joe' and exit.",
    )

    return parser.parse_args()


def main():
    """Main entry point for the CLI"""

    args = parse_args()

    log.basicConfig(
        format="%(levelname)s:%(module)s: %(message)s",
        level=[log.ERROR, log.INFO, log.WARNING, log.DEBUG][
            sum(args.log_level) if args.log_level else 0
        ],
    )

    if args.integrity_check:
        return cli_integrity_check(args)

    if args.produce_report:
        return cli_produce_report(args)

    if args.resources:
        return cli_resources(args)

    if args.example:
        return cli_example(args)

    if args.version:
        return cli_version(args)

    return cli_workflow(args)

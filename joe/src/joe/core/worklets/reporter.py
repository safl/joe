"""
    Report generator
    ================

    Generates a HTML report in the workflow output directory.

    Retargtable: false
    ------------------

    The report-generator works on the files generated by cijoe on the host which is
    executing cijoe. Thus, no need to make this re-targetable.


    Step arguments
    --------------

    # Whether or not the generated report should be opened (in a browser)
    report_open: true|false
"""
import json
import yaml
import pprint
import logging as log
import webbrowser
from pathlib import Path

import jinja2

from joe.core.resources import dict_from_yamlfile, get_resources


def augment_runlog(path: Path):
    """Produce a dict of command-dicts with paths to .output and .state files"""

    run = {}

    if not (path.is_dir() and path.exists()):
        return run

    for cmd_path in sorted(path.glob("cmd_*.*")):
        stem = cmd_path.stem
        suffix = cmd_path.suffix[1:]
        if suffix not in ["output", "state"]:
            continue

        if stem not in run:
            run[stem] = {
                "output_path": None,
                "output": "",
                "state": {},
                "state_path": None,
            }

        run[stem][f"{suffix}_path"] = cmd_path
        if suffix == "output":
            with run[stem][f"{suffix}_path"].open() as content:
                run[stem][f"{suffix}"] = content.read()
        elif suffix == "state":
            run[stem][f"{suffix}"] = dict_from_yamlfile(run[stem][f"{suffix}_path"])

    return run


def longrepr_to_string(longrepr):
    """Extract pytest crash/traceback info"""

    lines = []

    lines.append("# crashinfo")
    reprcrash = longrepr.get("reprcrash", {})
    for key, value in reprcrash.items():
        lines.append(f"{key}: {value}")

    entries = longrepr.get("reprtraceback", {"reprentries": []}).get("reprentries", [])
    for entry in entries:
        if entry is None:
            continue

        data = entry.get("data")
        if data is None:
            continue

        reprfuncargs = data.get("reprfuncargs")
        if reprfuncargs is None:
            continue

        reprargs = reprfuncargs.get("args")
        if reprargs is None:
            continue

        lines.append("")
        lines.append("# test-args")

        for argline in reprargs:
            lines.append(":".join(argline))

        lines.append("")
        lines.append("# test-output-lines")
        for dataline in entry.get("data", {"lines": []}).get("lines", []):
            lines.append(dataline)

    return "\n".join(lines)


def augment_testreport(path: Path):
    """Parse the given testfile into a list of "tests"""

    results = {
        "status": {"failed": 0, "passed": 0, "skipped": 0, "total": 0},
        "tests": {},
    }

    logpath = path / "testreport.log"
    if not logpath.exists():
        return {}

    with logpath.open() as logfile:
        for count, line in enumerate(logfile.readlines()):
            result = json.loads(line)
            if result["$report_type"] != "TestReport":
                continue

            nodeid = result["nodeid"]
            if nodeid not in results["tests"]:
                try:
                    comp = nodeid.split("::")
                    group_left = comp[0]
                    group_right = "".join(comp[1:])
                except Exception:
                    group_left, group_right = (nodeid, nodeid)

                results["tests"][nodeid] = {
                    "group_left": group_left,
                    "group_right": group_right,
                    "count": count,
                    "nodeid": nodeid,
                    "duration": 0.0,
                    "outcome": [],
                    "runlog": {},
                    "longrepr": "",
                }
            if isinstance(result["longrepr"], list):
                results["tests"][nodeid]["longrepr"] += "\n".join(
                    [str(item) for item in result["longrepr"]]
                )
            elif isinstance(result["longrepr"], dict):
                results["tests"][nodeid]["longrepr"] += longrepr_to_string(
                    result["longrepr"]
                )

            results["tests"][nodeid]["duration"] += result["duration"]
            results["tests"][nodeid]["outcome"] += [result["outcome"]]

            runlog = augment_runlog(path / result["nodeid"])
            if runlog:
                results["tests"][nodeid]["runlog"] = runlog

    for nodeid, testcase in results["tests"].items():
        results["status"]["total"] += 1
        for key in ["failed", "skipped", "passed"]:
            if key in testcase["outcome"]:
                results["status"][key] += 1
                break

    if results["status"]["total"]:
        return results

    return {}


def worklet_entry(args, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    report_open = step.get("with", {"report_open": True}.get("report_open", True))

    resources = get_resources()

    template_path = resources["templates"]["core.report-workflow"].path
    report_path = args.output / "report.html"

    log.info(f"template: {template_path}")
    log.info(f"report: {report_path}")

    workflow_state = dict_from_yamlfile(args.output / "workflow.state")
    workflow_state["config"] = cijoe.config.options

    for step in workflow_state["steps"]:
        if "extras" not in step:
            step["extras"] = {}

        step_path = args.output / step["id"]
        if not step_path.exists():
            continue

        runlog = augment_runlog(step_path)
        if runlog:
            step["extras"]["runlog"] = runlog

        testreport = augment_testreport(step_path)
        if testreport:
            step["extras"]["testreport"] = testreport

    template = jinja2.Environment(
        autoescape=True, loader=jinja2.FileSystemLoader(template_path.parent)
    ).get_template(template_path.name)

    with (report_path).open("w") as report:
        report.write(template.render(workflow_state))

    if report_open:
        webbrowser.open(str(report_path))

    return 0

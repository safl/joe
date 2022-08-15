import json
import pprint
from pathlib import Path

import jinja2

from joe.core.misc import dict_from_yaml, h2, h3


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
            run[stem][f"{suffix}"] = dict_from_yaml(run[stem][f"{suffix}_path"])

    return run


def augment_testreport(path: Path):
    """Parse the given testfile into a list of "tests"""

    results = {}

    logpath = path / "testreport.log"
    if not logpath.exists():
        return results

    with logpath.open() as logfile:
        for count, line in enumerate(logfile.readlines()):
            result = json.loads(line)
            if result["$report_type"] != "TestReport":
                continue

            nodeid = result["nodeid"]
            if nodeid not in results:
                results[nodeid] = {
                    "count": count,
                    "nodeid": nodeid,
                    "duration": 0.0,
                    "outcome": [],
                    "run.log": {},
                }
            results[nodeid]["duration"] += result["duration"]
            results[nodeid]["outcome"] += [result["outcome"]]

            runlog = augment_run(path / result["nodeid"])
            if runlog:
                results[nodeid]["runlog"] = runlog

    return results


def worklet_entry(args, collector, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    # template_path = collector.resources["templates"]["core.report-workflow"].path
    template_path = collector.resources["templates"]["report-workflow"].path
    report_path = args.output / "report.html"

    print(f"template: {template_path}")
    print(f"report: {report_path}")
    h3()

    workflow_state = dict_from_yaml(args.output / "workflow.state")
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

    return 0

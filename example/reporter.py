import json
import pprint

import jinja2

from joe.core.misc import dict_from_yaml, h2, h3


def populate_logs(args, collector, cijoe, step, workflow_state):

    logfiles = ["run.log", "pytest.log"]

    for step, filename in [
        (step, filename) for step in workflow_state["steps"] for filename in logfiles
    ]:
        if "logs" not in step:
            step["logs"] = {}

        path = args.output / step["id"] / filename
        if not path.exists():
            continue

        step["logs"][filename] = {"path": path, "content": ""}

        with path.open() as logfile:
            if filename == "pytest.log":
                results = {}

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
                            "run.log": "",
                        }
                    results[nodeid]["duration"] += result["duration"]
                    results[nodeid]["outcome"] += [result["outcome"]]

                    runlog_path = (
                        args.output / step["id"] / result["nodeid"] / "run.log"
                    )
                    if runlog_path.exists():
                        results[nodeid]["run.log"] = runlog_path

                for nodeid, result in results.items():
                    if "failed" in result["outcome"]:
                        result["status"] = "failed"
                    elif "skipped" in result["outcome"]:
                        result["status"] = "skipped"
                    elif "passed" in result["outcome"]:
                        result["status"] = "passed"
                    else:
                        result["status"] = "unknown"

                step["logs"][filename]["tests"] = results
            else:
                step["logs"][filename]["content"] = logfile.read()


def worklet_entry(args, collector, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    template_path = collector.resources["templates"]["report-workflow"].path
    report_path = args.output / "report.html"

    print(f"template: {template_path}")
    print(f"report: {report_path}")
    h3()

    workflow_state = dict_from_yaml(args.output / "workflow.state")

    populate_logs(args, collector, cijoe, step, workflow_state)

    template = jinja2.Environment(
        autoescape=True, loader=jinja2.FileSystemLoader(template_path.parent)
    ).get_template(template_path.name)

    with (report_path).open("w") as report:
        report.write(template.render(workflow_state))

    return 0

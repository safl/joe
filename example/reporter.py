import jinja2
import pprint
import json
from joe.core.misc import h2, h3, dict_from_yaml


def populate_logs(args, collector, cijoe, step, workflow_state):

    logfiles = ["run.log", "pytest.log"]

    for step, filename in [(step, filename) for step in workflow_state["steps"] for filename in logfiles]:
        if "logs" not in step:
            step["logs"] = {}

        path = args.output / step["id"] / filename
        if not path.exists():
            continue

        step["logs"][filename] = {"path": path, "content": ""}

        with path.open() as logfile:
            if filename == "pytest.log":
                step["logs"][filename]["tests"] = []

                for line in logfile.readlines():
                    result = json.loads(line)
                    if result["$report_type"] != "TestReport":
                        continue

                    runlog_path = args.output / step["id"] / result["nodeid"] / "run.log"
                    if runlog_path.exists():
                        result["run.log"] = runlog_path

                    step["logs"][filename]["tests"].append(result)
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
        autoescape=True,
        loader=jinja2.FileSystemLoader(template_path.parent)
    ).get_template(template_path.name)

    with (report_path).open("w") as report:
        report.write(template.render(workflow_state))

    return 0

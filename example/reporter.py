import jinja2
import pprint
import json
from joe.core.misc import h2, h3, dict_from_yaml

def load_pytest_reportlog(args, step):

    path = (args.output / step["id"] / "pytest.log")
    if not path.exists():
        return []

    tests = []
    with path.open() as logfile:
        for line in logfile.readlines():
            result = json.loads(line)

            if result["$report_type"] != "TestReport":
                continue

            runlog_path = args.output / step["id"] / result["nodeid"] / "run.log"
            if runlog_path.exists():
                result["run.log"] = runlog_path

            tests.append(result)

    return tests

def worklet_entry(args, collector, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    template_path = collector.resources["templates"]["report-workflow"].path
    report_path = args.output / "report.html"

    print(f"template: {template_path}")
    print(f"report: {report_path}")
    h3()

    workflow_state = dict_from_yaml(args.output / "workflow.state")

    # Add auxilary information
    for step in workflow_state["steps"]:
        runlog_path = (args.output / step["id"] / "run.log")
        step["run.log"] = runlog_path if runlog_path.exists() else None

        step["pytest"] = load_pytest_reportlog(args, step)

    # Render
    template = jinja2.Environment(
        autoescape=True,
        loader=jinja2.FileSystemLoader(template_path.parent)
    ).get_template(template_path.name)

    with (report_path).open("w") as report:
        report.write(template.render(workflow_state))

    return 0

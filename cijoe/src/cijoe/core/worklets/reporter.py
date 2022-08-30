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
import logging as log
import webbrowser

import jinja2
import yaml

from cijoe.core.processing import process_workflow_output
from cijoe.core.resources import get_resources


def to_yaml(value):
    return yaml.dump(value)


def worklet_entry(args, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    report_open = step.get("with", {"report_open": True}.get("report_open", True))

    resources = get_resources()

    template_path = resources["templates"]["core.report-workflow"].path
    report_path = args.output / "report.html"

    log.info(f"template: {template_path}")
    log.info(f"report: {report_path}")

    workflow_state = process_workflow_output(args, cijoe)

    jinja_env = jinja2.Environment(
        autoescape=True, loader=jinja2.FileSystemLoader(template_path.parent)
    )
    jinja_env.filters["to_yaml"] = to_yaml
    template = jinja_env.get_template(template_path.name)

    with (report_path).open("w") as report:
        report.write(template.render(workflow_state))

    if report_open:
        webbrowser.open(str(report_path))

    return 0

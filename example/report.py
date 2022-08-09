import jinja2
from joe.core.misc import h2, h3, dict_from_yaml


def worklet_entry(args, collector, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    template_path = collector.resources["templates"]["report-workflow"].path
    report_path = args.output / "report.html"

    print(f"template: {template_path}")
    print(f"report: {report_path}")
    h3()

    workflow_state = dict_from_yaml(args.output / "workflow.state")

    template = jinja2.Environment(
        autoescape=True,
        loader=jinja2.FileSystemLoader(template_path.parent)
    ).get_template(template_path.name)

    with (report_path).open("w") as report:
        report.write(template.render(workflow_state))

    return 0

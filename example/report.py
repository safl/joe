import jinja2
from joe.core.misc import h2, h3, dict_from_yaml


def worklet_entry(args, collector, cijoe, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    template_path = collector.resources["templates"]["report-workflow"].path

    print(f"template: {template_path}")
    h3()

    template = jinja2.Environment(
        autoescape=True,
        loader=jinja2.FileSystemLoader(template_path.parent)
    ).get_template(template_path.name)

    with (args.output / "report.html").open("w") as report:
        report.write(template.render(dict_from_yaml(args.output / "workflow.state")))

    return 0

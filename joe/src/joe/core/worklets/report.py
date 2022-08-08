from pathlib import Path

import jinja2
import yaml

from joe.core.resources import Collector


def worklet_entry(cijoe, args, step):
    """Produce a HTML report of the 'workflow.state' file in 'args.output'"""

    # NOTE: cijoe should already have a collector-instance to use...
    collector = Collector()
    collector.collect()

    # Load the workflow-state
    state_path = args.output / "workflow.state"
    with state_path.open() as state_file:
        state = yaml.load(state_file, Loader=yaml.SafeLoader)

    # Instantiate jinja2 template
    template_resource = collector.resources["templates"]["core.report"]
    template = jinja2.Environment(
        autoescape=True, loader=jinja2.FileSystemLoader(template_resource.path.parent)
    ).get_template(template_resource.path.name)

    # Render template using workflow-state as data and write it to file
    with (args.output / "report.html").open("w") as report_file:
        report_file.write(template.render(state))

    return 0

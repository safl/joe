import pprint
import re

import yaml
from joe.core.command import Cijoe, env_from_file


# TODO:
# * Implement this
# * Move this into the core package
def workflow_lint(args):
    """Do integrity-check of workflow"""

    return True


# TODO:
# * Add use of the test-linter before attempting to run the workflow
# * Move this into the core package
# * Add error-handling
def workflow_run(args):
    """Run workflow"""

    with open(args.workflow) as workflow_file:
        workflow = yaml.load(workflow_file, Loader=yaml.SafeLoader)

    joe = Cijoe(env_from_file(args.env), args.output)

    count = 0
    for entry in workflow.get("steps", []):
        count += 1
        step = {
            "count": count,
            "name": "",
            "name_fs": "",
            "run": "",
            "with": "",
            "uses": {},
        }

        step["name"] = entry.get("name", "") if entry.get("name") else "unnamed step"
        step["name"] = f"{step['count']}_{step['name']}"
        step["name_fs"] = re.sub(
            r"[\(\)\.\s/\\?%*:|\"<>\x7F\x00-\x1F]", "_", step["name"]
        )

        joe.set_output_ident(step["name_fs"])

        if "uses" in entry:
            step["uses"] = entry.get("uses")
            step["with"] = entry.get("with", {})

            pprint.pprint(step)

            args.worklets[step["uses"]](None, args, step)
        elif "run" in entry:
            step["run"] = entry.get("run").strip().splitlines()
            for cmd in step["run"]:
                joe.run(cmd)
        else:
            print("invalid step-definition")
            return 1

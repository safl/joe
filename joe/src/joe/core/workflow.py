import pprint
import re

import yaml

from joe.core.command import Cijoe, env_from_file


# TODO:
# * Implement this
def workflow_lint(args):
    """Do integrity-check of workflow"""

    return True


# TODO:
# * Add use of the test-linter before attempting to run the workflow
# * Add error-handling
# * Improve the path-mangling for the cijoe-instance, especially when delegated to
#   worklets
def workflow_run(args):
    """Run workflow"""

    with open(args.workflow) as workflow_file:
        workflow = yaml.load(workflow_file, Loader=yaml.SafeLoader)

    joe = Cijoe(env_from_file(args.env) if args.env else {}, args.output)

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

        if "uses" in entry:
            step["uses"] = entry.get("uses")
            step["with"] = entry.get("with", {})
            step["type"] = "worklet"
        elif "run" in entry:
            step["type"] = "run"
            step["run"] = entry.get("run").strip().splitlines()
        else:
            print("invalid step-definition")
            return 1

        foo = step["uses"] if step["uses"] else "inline"

        step["name"] = f"{step['count']}_{step['type']}_{foo}_{step['name']}"
        step["name_fs"] = re.sub(
            r"[\(\)\.\s/\\?%*:|\"<>\x7F\x00-\x1F]", "_", step["name"]
        ).lower()
        joe.set_output_ident(step["name_fs"])

        if step["type"] == "run":
            for cmd in step["run"]:
                joe.run(cmd)
        elif step["type"] == "worklet":
            args.worklets[step["uses"]](joe, args, step)

import pprint
from pathlib import Path
import re

import yaml

from joe.core.command import Cijoe, config_from_file

WORKFLOW_SUFFIX = "workflow"


# TODO:
# * Implement this
def workflow_lint(args):
    """Do integrity-check of workflow"""

    return True


def paths_to_workflow_fpaths(paths):
    """Return list of workflow files in the given list of files and directories"""

    workflow_files = []
    for path in [Path(p).resolve() for p in paths]:
        if path.is_dir():
            workflow_files.extend(
                [p for p in path.iterdir() if p.name.endswith(f".{WORKFLOW_SUFFIX}")]
            )
        elif path.is_file() and path.name.endswith(f".{WORKFLOW_SUFFIX}"):
            workflow_files.append(path)

    return workflow_files

# TODO:
# * Add use of the test-linter before attempting to run the workflow
# * Add error-handling
# * Improve the path-mangling for the cijoe-instance, especially when delegated to
#   worklets
def run_workflow_files(args):
    """Run workflow"""

    joe = Cijoe(config_from_file(args.config) if args.config else {}, args.output)

    for workflow_fpath in paths_to_workflow_fpaths(args.file_or_dir):

        with open(workflow_fpath) as workflow_file:
            workflow = yaml.load(workflow_file, Loader=yaml.SafeLoader)

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

            step["name"] = (
                entry.get("name", "") if entry.get("name") else "unnamed step"
            )

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

    return 0
